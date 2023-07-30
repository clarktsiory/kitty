import dbus

bus = dbus.SessionBus()

class Player:

  _instance = None

  _DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'
  _MEDIA_PLAYER = 'org.mpris.MediaPlayer2.Player'

  def __init__(self, status, metadata):
      self._status = status
      self._metadata = metadata
      print(status)
      print(metadata)

  @property
  def status(self):
      return self._status

  @property
  def metadata(self):
      return self._metadata

  @property
  def is_playing(self):
      return False

  @property
  def is_paused(self):
      return False

  @property
  def title(self):
      return ""

  @property
  def artist(self):
      return ""

  def _from_session_bus(session_bus):
      status = session_bus.Get(Player._MEDIA_PLAYER, 'PlaybackStatus', dbus_interface=Player._DBUS_INTERFACE)
      metadata = session_bus.Get(Player._MEDIA_PLAYER, 'Metadata', dbus_interface=Player._DBUS_INTERFACE)
      return Player(status, metadata)

  def get_instance():
    if Player._instance is not None:
        return Player._instance

    for service in bus.list_names():
      if service.startswith('org.mpris.MediaPlayer2.'):
        Player._instance = Player._from_session_bus(dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2'))
        return Player._instance

    raise OSError("Media player not found")
