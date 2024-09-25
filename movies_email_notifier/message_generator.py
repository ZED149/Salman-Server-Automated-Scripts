

# this file includes the MessageGenerator class


class MessageGenerator:
    # private variables
    __signature = '''\
    <hr style="height10px">
    <table>
            <tr>
                <td bgcolor="#00A4BD" align="center" style="color: white;">
                    <h1>ZED</h1>
                </td>
                <td align="center" style="padding: 10px 0 0 10px;">
                    <img src="cid:image1" height=50px width=50/>
                </td>
            </tr>
    </table><br>
<label>Contact us: </label><span><a href="https://www.zed149.com">Support</a></span>
<p>Thanks for your order.</p>
'''

    # Methods

    @classmethod
    # no_reply_movies_added
    def no_reply_movies_added(cls, receiver_name: str, list_of_movies: list) -> str:
        """
        Returns a message containing the name of the receiver.
        :param receiver_name: Name of the receiver.
        :param list_of_movies: List containing name of movies to iterate and append on.
        :return message: Final string that contains the whole email body
        """

        # writing styles for our message
        # message string
        fs = 'font-size:56px'
        fs2 = 'font-size:28px;font-weight:900'
        fw = 'font-weight:100'
        va = 'vertical-align:top'
        check = 'margin:auto;width:600px;background-color:#fff'

        # before part of the message string to send on email
        message = f'''\
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
          h1{fs}
          h2{fs2}
          p{fw}
          td{va}
          #email{check}
        </style>
    </head>
    <body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
    <div id="email">
        <table role="presentation" width="100%">
            <tr>
                <td bgcolor="#00A4BD" align="center" style="color: white;">
                    <h1> ZED</h1>
                </td>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
            <tr>
                <td>
                    <h2>Hurrah! {receiver_name}. New movies have been uploaded to the server.</h2>
                    <h3>Feel free to check them out at anytime you want</h3>
                    <p>
                        <ol>
'''
        
        # appending list_of_movies with the string
        for movie in list_of_movies:
            message = message + f'<li>{movie}</li>'
        
        # writing the after part of the email
        message = message + '''\
                        </ol>
                    </p>
                </td>
            </tr>
        </table>
        <hr>
        <table width="100%" role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
            <tr>
                <td>
                    <strong><h5>This is a server generated email. Please donot reply to this email as your replies will not be viewed.
                    </h5></strong>
                    <h6>In case of any suggestions or query. Feel free to contact support at salmanahmad@zed149.com</h6>
                </td>
            </tr>
        </table>
'''

        closing_remarks = '''</div>
    </body>
</html>'''
        # adding signature to the message
        message = message + cls.__signature
        # closing the html file
        message = message + closing_remarks

        # Return
        return message
    
