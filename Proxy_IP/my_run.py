from study_crawler.Proxy_IP.my_scheduler import Scheduler

def main():
    """在这里启动整个代理池"""
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        print('主程序mian错误重新调用', e.args)
        main()

if __name__ == '__main__':
    main()