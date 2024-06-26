from domjudge_tool_cli.utils.email.smtp import SMTP


class CustomSMTP(SMTP):

    def open(self):
        connection_params = dict()
        if self.timeout is not None:
            connection_params["timeout"] = self.timeout

        self.connection = self.connection_class(
            self.host, self.port, **connection_params
        )
        self.connection.ehlo()

        if not self.use_ssl:
            self.connection.starttls()

        if self.username and self.password:
            self.connection.login(self.username, self.password)