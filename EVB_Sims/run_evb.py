if __name__ == "__main__":
    import json
    import shutil
    from pathlib import Path
    from datetime import datetime
    from time import perf_counter
    from argparse import ArgumentParser

    import numpy as np

    from sim.evb import evb_analysis
    from sim import prepare_evb_tasks, run_evb_batch

    import random
 
    # Generates a random number between
    # a given positive range
    r1 = random.randint(0, 100)

    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument('per_gpu', type=int, default=1, help='Number of tasks per GPU')
    args = parser.parse_args()

    # Make a test directory to store EVB results
    evb_dir = Path('evb_files')
    evb_test_dir = Path(f"evb-test-run-{r1}-{args.per_gpu}").absolute()
    if evb_test_dir.exists():
        shutil.rmtree(evb_test_dir)
    evb_test_dir.mkdir(parents=True)

    # Read our input files from disk
    pdb = (evb_dir / '2pwz_G.pdb').read_text()
    ref_pdb = (evb_dir / '5mdh_b.pdb').read_text()
    template_yml = (evb_dir / 'template.yml').absolute()
    lig_yml = (evb_dir / 'lig.yml').absolute()
    start_time = perf_counter()
    md_yamls = prepare_evb_tasks(Path(evb_test_dir), pdb, ref_pdb, lig_yml, template_yml)
    setup_time = perf_counter() - start_time

    # Run YAMLs
    md_count = len(md_yamls)
    start_time = perf_counter()
    assert len(md_yamls) > args.per_gpu * 12
    sim_paths = run_evb_batch(evb_test_dir, md_yamls[:12 * args.per_gpu], tasks_per_gpu=args.per_gpu, n_gpus=12)
    md_time = perf_counter() - start_time

    # Perform the EVB computation
    start_time = perf_counter()
    pmf = evb_analysis(sim_paths)
    wham_time = perf_counter() - start_time
    np.save(str(evb_test_dir / 'pmf.npy'), pmf)

    # Save the runtime information
    with open('runtimes.json', 'a') as fp:
        print(json.dumps({
            'time': datetime.now().isoformat(),
            'per_gpu': args.per_gpu,
            'md_count': md_count,
            'setup_time': setup_time,
            'md_time': md_time,
            'wham_time': wham_time,
        }), file=fp)
