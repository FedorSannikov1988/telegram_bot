import asyncio
import time


async def fun1(x):
    print('fun1 начата')
    print(x**2)
    await asyncio.sleep(10)
    print('fun1 завершена')


async def fun2(x):
    print('fun2 начата')
    print(x**0.5)
    await asyncio.sleep(10)
    print('fun2 завершена')


async def main():
    task1 = asyncio.create_task(fun1(4))
    task2 = asyncio.create_task(fun2(4))
    await asyncio.gather(task1, task2)

print(time.strftime('%X'))
asyncio.run(main())
print(time.strftime('%X'))
