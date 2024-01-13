import asyncio
from repository import TokenRepository
from connections import get_session
# Optional for beautiful output
# from colorama import Fore, Style


async def run():
    while True:
        session = anext(get_session())
        repo = TokenRepository(await session)
        await repo.delete_exp_token()
        
        """
        You can use bellow line of code instead of normal print for beautiful output: 

        print(f"{Fore.GREEN}Delete Expired Token Function Called!{Style.RESET_ALL}")
        """

        print("Delete Expired Token Function Called!")
        await asyncio.sleep(60 * 60)
        

if __name__ == '__main__':
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        exit()
