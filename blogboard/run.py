import os
import sys
from pathlib import Path

# Auto-set current working directory to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import argparse
from datetime import datetime, timezone, timedelta

# ── Load .env (GROQ_API_KEY etc.) ────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv is optional; export env vars manually if needed

import os
try:
    import sentry_sdk
    sentry_dsn = os.getenv("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
            _experiments={
                "continuous_profiling_auto_start": True,
            },
        )
except ImportError:
    pass

# ── Import compiled graph ─────────────────────────────────────────────────────
from blogboard.graph.graph import graph


# ─────────────────────────────────────────────────────────────────────────────

def today_ist() -> str:
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(
        description="BlogBoard LangGraph Article Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  # Generate today's article (IST):
  python blogboard/run.py

  # Generate article for a specific title/topic:
  python blogboard/run.py --topic "Building RAG Applications with LangChain" --domain "genai"

  # Generate AI news roundup:
  python blogboard/run.py --ainews

  # Dry run — preview topic/title selection without API writes:
  python blogboard/run.py --dry-run
        """,
    )
    parser.add_argument(
        "--topic", "--title", type=str, default=None,
        help="Target article title/topic to generate",
    )
    parser.add_argument(
        "--domain", type=str, default=None,
        help="Category domain (ml, dl, nlp, cv, genai, statistics, ainews)",
    )
    parser.add_argument(
        "--date", type=str, default=None,
        help="Target date in YYYY-MM-DD format (default: today in IST)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview mode: skip Groq calls and file writes",
    )
    parser.add_argument(
        "--ainews", action="store_true",
        help="Run the AI News gathering and generation graph",
    )
    parser.add_argument(
        "--serve", action="store_true",
        help="Start the FastAPI REST API Gateway & Background Scheduler Server",
    )
    args = parser.parse_args()

    if args.serve:
        import uvicorn
        print("\n🚀 Starting Agentic Blog Engine FastAPI Gateway & Background Scheduler...")
        print("🌐 Open http://localhost:8000/docs in your browser to view the API dashboard!\n")
        uvicorn.run("blogboard.api.app:app", host="127.0.0.1", port=8000, reload=False)
        return

    date_str = args.date or today_ist()
    dry_run  = args.dry_run
    run_ainews = args.ainews

    # ── Banner ────────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"  Agentic Blog Engine — LangGraph Multi-Agent Generator")
    print(f"  Date    : {date_str}")
    if args.topic:
        print(f"  Topic   : {args.topic}")
    if args.domain:
        print(f"  Domain  : {args.domain}")
    print(f"  Dry run : {dry_run}")
    print(f"{'='*55}")

    # ── Build initial state and invoke the graph ──────────────────────────────
    initial_state = {
        "date":    date_str,
        "dry_run": dry_run,
    }
    
    if args.topic:
        initial_state["topic"] = args.topic
    if args.domain:
        initial_state["domain"] = args.domain

    if run_ainews:
        initial_state["domain"] = "ainews"

    config = {"configurable": {"thread_id": "blogboard-1"}}
    # The single compiled graph is smart enough to route to NewsAgent if domain=='ainews'
    final_state = graph.invoke(initial_state, config=config)

    # Trigger notification dispatcher
    if not dry_run:
        from blogboard.services.dispatcher import dispatcher
        dispatcher.dispatch_all(final_state)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    if dry_run:
        print(f"  [DRY RUN] Pipeline completed — no files were written.")
        domain = final_state.get("domain", "?")
        topic  = final_state.get("topic", "?")
        slug   = final_state.get("slug", "?")
        print(f"  Chosen Domain : {domain}")
        print(f"  Chosen Topic  : {topic}")
        print(f"  Target Upload Path:")
        print(f"    -> blogs/{domain}/{slug}.md")
        print(f"    -> blogs/{domain}/articles.json")
    else:
        domain    = final_state.get("domain", "?")
        title     = final_state.get("title", "?")
        md_path   = final_state.get("md_path", "?")
        read_time = final_state.get("read_time", "?")
        print(f"  🎉 Done!  Article generated successfully.")
        print(f"  Title     : {title}")
        print(f"  Domain    : {domain}")
        print(f"  Read time : {read_time}")
        print(f"  File      : {md_path}")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
