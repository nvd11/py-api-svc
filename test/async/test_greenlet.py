# 导入 greenlet 库，用于创建和管理协程
from greenlet import greenlet
# 导入项目配置文件，这里虽然导入了但并未使用
import src.configs.config
# 导入 loguru 日志库，用于记录程序执行信息
from loguru import logger

# 定义第一个协程函数 func1
def func1():
    # 打印日志 "step 1"
    logger.info("step 1")
    # 切换到第二个协程 gl2 执行
    gl2.switch()
    # 从其他协程切换回来后，打印日志 "step 3"
    logger.info("step 3")
    # 再次切换到第二个协程 gl2 执行，以完成 func2 的剩余部分， 
    # 注意， 如果没有这行代码，func1 执行完成后不会自己返回func2,  func2 中的 "step 4" 将不会被执行
    gl2.switch()


# 定义第二个协程函数 func2
def func2():
    # 打印日志 "step 2"
    logger.info("step 2")
    # 切换回第一个协程 gl1 执行
    gl1.switch()
    # 从其他协程切换回来后，打印日志 "step 4"
    logger.info("step 4")


# 创建第一个协程对象 gl1，关联 func1 函数
gl1 = greenlet(func1)
# 创建第二个协程对象 gl2，关联 func2 函数
gl2 = greenlet(func2)



# 定义一个 pytest 测试函数
def test_greenlet():
     # 启动第一个协程 gl1，开始执行
     gl1.switch()
