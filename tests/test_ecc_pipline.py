
from pipelines.ecc_pipeline import create_runner, create_session, run_ecc_once, demo_input


def test_ecc_runs_smoke():
    runner = create_runner()
    session = create_session(runner)
    output = run_ecc_once(runner, session.id, demo_input())
    assert isinstance(output, str)
    assert len(output) > 0
