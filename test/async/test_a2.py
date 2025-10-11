import asyncio
import time

async def async_demo():
    print("异步: 开始任务A (3秒)")
    await asyncio.sleep(3)
    print("异步: 任务A完成")

async def main():
    start = time.time()
    
  
  
    
    await aysnc_demo()
    
    print(f"总时间: {time.time() - start:.1f}秒")

# 运行
def test_a2():
    asyncio.run(main())