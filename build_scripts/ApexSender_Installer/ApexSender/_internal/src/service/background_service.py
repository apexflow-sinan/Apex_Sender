import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.core.server_manager import ServerManager

logging.basicConfig(
    filename=str(Path.home() / '.apex_sender' / 'service.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ApexSenderService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ApexSenderService"
    _svc_display_name_ = "Apex Sender Service"
    _svc_description_ = "خدمة تشغيل Apex Sender في الخلفية"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.server_manager = None
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Service stop requested')

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        logging.info('Apex Sender Service starting...')
        try:
            self.server_manager = ServerManager()
            success, results = self.server_manager.start_all()
            
            if success:
                logging.info('All servers started successfully')
            else:
                logging.error(f'Failed to start servers: {results}')
            
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            
        except Exception as e:
            logging.error(f'Service error: {e}')
        finally:
            if self.server_manager:
                self.server_manager.stop_all()
            logging.info('Apex Sender Service stopped')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ApexSenderService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ApexSenderService)
