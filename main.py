
from pipelines.ecc_pipeline import create_runner, create_session, run_ecc_once, demo_input


def main():
    runner = create_runner()
    session = create_session(runner)

    briefing = run_ecc_once(
        runner=runner,
        session_id=session.id,
        user_message=demo_input(),
    )

    print("\n================ ECC BRIEFING ================\n")
    print(briefing)
    print("\n==============================================\n")


if __name__ == "__main__":
    main()
