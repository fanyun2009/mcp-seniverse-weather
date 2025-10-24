import asyncio


def number_generator(n):
    for i in range(n):
        yield i  # 返回 i 并暂停，下次调用从这里继续
        print(f"生成完 {i} 后继续")

async def async_number_generator(n):
    for i in range(n):
        await asyncio.sleep(1)  # 模拟异步操作（必须用 await）
        yield i  # 生成值并暂停

# 使用生成器
# gen = number_generator(3)
# print(next(gen))  # 输出 0，执行到 yield 暂停
# print("======")  # 输出 0，执行到 yield 暂停
# print(next(gen))  # 输出“生成完 0 后继续”，再输出 1，再次暂停

# 使用异步生成器
async def main():
    async for num in async_number_generator(3):
        print(num)
asyncio.run(main())



