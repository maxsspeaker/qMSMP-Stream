import desktop_notify
notify = desktop_notify.glib.Notify('summary', 'body')
notify.set_on_show(callback) # optional
notify.show()
