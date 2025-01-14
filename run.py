from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctabacktester import CtaBacktesterApp
from vnpy_datamanager import DataManagerApp

def main():
    """启动VeighNa Trader"""
    # 创建Qt应用对象
    qapp = create_qapp()

    # 创建事件引擎
    event_engine = EventEngine()

    # 创建主引擎
    main_engine = MainEngine(event_engine)

    # 添加应用模块
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(DataManagerApp)

    # 创建主窗口
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    # 在窗口显示后再加载应用模块
    qapp.processEvents()

    # 在主线程中启动Qt事件循环
    qapp.exec()


if __name__ == "__main__":
    # 打印欢迎信息
    print("欢迎使用VeighNa Trader")
    main()
