import platform

def notify(summary, body='', app_name='', app_icon='',
           timeout=5000, actions=[], hints=[], replaces_id=0):
  if platform.system() == 'Linux':
    notify_linux(summary, body, app_name, app_icon, timeout, actions, hints, replaces_id)
  elif platform.system() == 'Darwin':
    notify_mac(summary, body, app_name, app_icon, timeout, actions, hints, replaces_id)

def notify_linux(summary, body='', app_name='', app_icon='',
    timeout=5000, actions=[], hints=[], replaces_id=0):
  import dbus
  import sys
  _bus_name = 'org.freedesktop.Notifications'
  _object_path = '/org/freedesktop/Notifications'
  _interface_name = _bus_name

  session_bus = dbus.SessionBus()
  obj = session_bus.get_object(_bus_name, _object_path)
  interface = dbus.Interface(obj, _interface_name)
  interface.Notify(app_name, replaces_id, app_icon,
      summary, body, actions, hints, timeout)


def notify_mac(summary, body='', app_name='', app_icon='',
               timeout=5000, actions=[], hints=[], replaces_id=0):
  from Foundation import NSUserNotification
  from Foundation import NSUserNotificationCenter
  from Foundation import NSUserNotificationDefaultSoundName
  notification = NSUserNotification.alloc().init()
  notification.setTitle_(summary)
  notification.setInformativeText_(body)
  notification.setSoundName_(NSUserNotificationDefaultSoundName)
  #notification.setImage("svd.jpg")
  center = NSUserNotificationCenter.defaultUserNotificationCenter()
  center.deliverNotification_(notification)



# If run as a script, just display the argv as summary
if __name__ == '__main__':
  notify(summary=' '.join(sys.argv[1:]))
