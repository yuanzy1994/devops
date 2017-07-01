from config import settings
import api


def start_auth():
    # type: (object) -> object
    #account = settings.login_info
    if settings.login_info.get('user') == 'root'  and settings.login_info.get('passwd') == 'pass':
        print "auth OK!"
        api.select()

    else:
        print "auth FAILED!"




