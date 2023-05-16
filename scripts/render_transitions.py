from aiogram_dialog.tools import render_transitions

from src.routers.main import main_router


async def main():
    render_transitions(main_router,
                       title="Bot Transitions",
                       filename="out/transitions",
                       format=["png", "svg", "dot"])  # noqa


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
