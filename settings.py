EMAIL_USE_LOCALTIME = True

#for unitest
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com' #可以换其他邮箱
EMAIL_PORT = 465
#994/465/587
EMAIL_HOST_USER = 'your email username'
EMAIL_HOST_PASSWORD = 'your email password or code'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

CORPID="your corpid"  # 企业 ID
APPID="your appid"  # 企业应用 ID
CORPSECRET="your corpsecret" # 企业应用 Secret
