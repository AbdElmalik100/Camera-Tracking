import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SecurityAlertActions:
    """
    TODO NOTE: I've found that you have to loging in the browser first. Which is not good way. 
    Secutiry alert for sending alert, emails, etc.
    You must loging first to your email and we advice you to generate a password from Google AppPasswordsGenerator.
    Link: `https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&followup=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&ifkv=ASKXGp2IIaHxVmP0pnP2q8lOm3wG31J8kHVZWW571Pn5N9kMzEfSrGtArsINQiujx43-ezp88TI4vg&osid=1&passive=1209600&rart=ANgoxcdJc2Rk0Zxjl-_7cR_bivagoBUo2ELtDBejOJL7mDHk9yUe08PI38vw7gkea6XI3dmEVxq9kAgokHJv0bE5E58jGWR7ow&service=accountsettings&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S1107723359%3A1705865451449927&theme=glif` 
    Attributes:
        password : str = The password you generated from Google to sign in to your accout
        from_email : str = The email you used to sign in to your account and generate the password
    """
    def __init__(self,password:str = "myvu jwhz earn pbuo", from_email:str = "eslam760000@gmail.com") -> None:
        """
        Initialize the class.
        Note that it will automatically sign in to your provided account after initialization.
        Parameters:
            password : str = The password you generated from Google to sign in to your accout
            from_email : str = The email you used to sign in to your account and generate the password
        """
        self.__from_email = from_email
        self.__password = password
        self.mail_sent = False
        
    def connect_to_server(self) -> None:
        self.server = smtplib.SMTP('smtp.gmail.com: 587')
        self.server.starttls()
        self.server.login(self.__from_email, self.__password)
        
    def send_email(self, message_body:str, to_email:str = "eslam7600000@gmail.com", subject:str = "Tracker Dashboard Warning") -> None:
        """
        Security Alert by sending an Email to your provided email.
        Parameters:
            message_body : str = The body of the email you want to send.
            to_email : str = The email you want to send the email(The Warning) to.
            subject: str (default = "Tracker Dashboard Warning") = Generar subject of the Warning.
        """
        try: self.connect_to_server()
        except: pass
        
        message = MIMEMultipart()
        message['From'] = self.__from_email
        message['To'] = to_email
        message['Subject'] = subject
        
        if (not self.mail_sent):
            message.attach(MIMEText(message_body, 'plain'))
            self.server.sendmail(self.__from_email, to_email, message.as_string())
            self.mail_sent = True
            print("Email Sent.....")
        else:
            print("Email Already Sent.....")
