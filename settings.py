EMAIL_USE_LOCALTIME = True

#for unitest
EMAIL_BACKEND = 'djangomail.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'djangomail.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com' #可以换其他邮箱
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your-username'
EMAIL_HOST_PASSWORD = '********'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER