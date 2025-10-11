import src.configs.config
from loguru import logger
import asyncio
import time

# 模拟网络请求
async def async_request(name, seconds):
    print(f"{name} 开始 - 需要 {seconds}秒")
    await asyncio.sleep(seconds)  # 异步等待
    print(f"{name} 完成")
    return f"{name}结果"

def sync_request(name, seconds):
    print(f"{name} 开始 - 需要 {seconds}秒")
    time.sleep(seconds)  # 同步阻塞
    print(f"{name}完成")
    return f"{name}结果"

#  异步版本 - 并发执行
async def async_demo():
    print("=== 异步并发执行 ===")
    start = time.time()
    
    # 同时启动3个任务
    task1 = async_request("下载图片", 2)
    task2 = async_request("查询数据库", 3)
    task3 = async_request("调用API", 1)
    
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)
    
    total_time = time.time() - start
    print(f"异步总耗时: {total_time:.1f}秒\n")
    return results

# 同步版本 - 顺序执行  
def sync_demo():
    print("=== 同步顺序执行 ===")
    start = time.time()
    
    # 一个接一个执行
    result1 = sync_request("下载图片", 2)
    result2 = sync_request("查询数据库", 3)
    result3 = sync_request("调用API", 1)
    
    total_time = time.time() - start
    print(f"同步总耗时: {total_time:.1f}秒\n")
    return [result1, result2, result3]

# 运行测试
async def test_a2():
    # 先测试异步
    await async_demo()
    
    # 再测试同步
    sync_demo()


def  test_a1():
    asyncio.run(test_a2())

