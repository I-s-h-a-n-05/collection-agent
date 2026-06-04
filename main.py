# main.py
from apscheduler.schedulers.blocking import BlockingScheduler
from agent.logger import init_db
from agent.scheduler import run_collection_cycle

def main():
    # 1. Boot
    init_db()

    # 2. Run immediately on startup — no waiting for first scheduled fire
    run_collection_cycle()

    # 3. Schedule daily at 09:00 local time
    scheduler = BlockingScheduler()
    scheduler.add_job(run_collection_cycle, "cron", hour=9, minute=0)

    print("[Main] Scheduler running. Daily at 09:00. Press Ctrl+C to stop.\n")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n[Main] Stopped.")

if __name__ == "__main__":
    main()