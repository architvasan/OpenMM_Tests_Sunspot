"""Workflow-compatible interfaces to the simulation tasks"""
import os
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

from joblib.externals.loky import ProcessPoolExecutor
from yaml import safe_load

from .evb import evb_setup, evb_ymls
from . import config
from .run import sim
from utils.pinning import get_persistent_process_pool

logger = logging.getLogger(__name__)


def prepare_evb_tasks(
        run_directory: Path,
        pdb: str,
        ref_pdb: str,
        lig_yml: Path,
        template_yml: Path
) -> list[Path]:
    """Generate the series of configuration files which define an EVB computation

    Args:
        run_directory: Directory in which to save the files
        pdb: PDB of sequence to be studied
        ref_pdb: PDB of reference structure
        lig_yml: Path to the configuration file describing the ligands
        template_yml: Path to the template used when generating MD runs
    Returns:
        A list of paths to the YAML files which define an EVB computations
    """

    start_dir = Path().cwd()
    try:
        os.chdir(run_directory)

        # Write the PDB to disk, as expected by
        pdb_path = Path(run_directory) / 'new.pdb'
        pdb_path.write_text(pdb)
        ref_pdb_path = Path(run_directory) / 'ref.pdb'
        ref_pdb_path.write_text(ref_pdb)

        # Generate the simulation setups
        sim_setups = evb_setup(str(pdb_path.relative_to(run_directory)),
                               str(ref_pdb_path.relative_to(run_directory)),
                               lig_yml, config.PYMOL_PATH)

        # Generate the yaml files defining the MD simulations
        md_ymls = evb_ymls(template_yml, sim_setups)
        return [Path(p) for p in md_ymls]
    finally:
        os.chdir(start_dir)  # Ensure we go back to the starting directory


def _run_in_directory(run_directory: Path, function: Callable, *args, **kwargs) -> object:
    """Run a function in a specific directory

    Args:
        run_directory: Directory in which to run
        function: Function to be invoked
        args, kwargs: Arguments to function
    Returns:
        Output from the function
    """
    start_dir = Path.cwd()
    try:
        os.chdir(run_directory)
        return function(*args, **kwargs)
    finally:
        os.chdir(start_dir)


def run_evb_batch(run_directory: Path, md_ymls: list[Path], n_gpus: int = 12, tasks_per_gpu: int = 1) -> list[Path]:
    """Run a batch of MD simulations that are part of an EVB run

    Each MD simulation is pinned to a different GPU and ran in
    the local storage of a compute node.

    Args:
        run_directory: Directory in which to archive the MD run data
        md_ymls: List of YAML files describing the MD computations we must perform
        n_gpus: Number of GPUs available to this computation
        tasks_per_gpu: Number of tasks per GPU (> 1 requires MPS)
    Returns:
        Path to the completed simulations
    """

    # Get the pool on which to run these MD computations
    pool = get_persistent_process_pool(n_gpus=n_gpus, tasks_per_gpu=tasks_per_gpu)

    return run_evb_in_parallel(md_ymls, pool, run_directory)


def run_evb_in_parallel(md_ymls: list[Path], pool: ProcessPoolExecutor, run_directory: Path, gpu: int | None = None, timeout: float = None) -> list[Path]:
    """Run a batch of EVB computations in parallel with each other on the same GPU

    Args:
        md_ymls: YAML files defining the runs
        pool: Process pool to use for the parallelism
        run_directory: Directory in which to run the computations
        gpu: Which GPU to use for computations, if pinning is required
        timeout: How long to wait for results before stopping work and raising TimeoutError
    Returns:
        Paths to the completed simulations
    """
    # Create a temporary folder in which to run the computations
    with TemporaryDirectory() as tmpdir:
        # Load the YAMLs, modify the SSD path, then submit it to execute
        futures = []
        for path in md_ymls:
            with path.open() as fp:
                sim_config = safe_load(fp)
            sim_config['local_ssd'] = tmpdir

            if gpu is not None:
                sim_config['gpu_id'] = gpu

            futures.append(pool.submit(_run_in_directory, run_directory, sim, sim_config))

        # Wait for them to complete
        output = []
        for future in futures:
            try:
                exception = future.exception(timeout=timeout)
            except TimeoutError:
                logger.info('Timeout reached for MD run. Killing jobs then exiting')
                raise

            if exception is not None:
                logger.warning(f'EVB run failed due to {str(exception)}')
            else:
                output.append(future.result())
        return output
