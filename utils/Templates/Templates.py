class Email():
    url = ""

    def __init__(self, url) -> None:
        self.url = url


class ActivateEmail(Email):
    def create_mail(self) -> str:
        file_content = """<body
	style="
		background-color: #eeeeee;
		padding: 5%;
		font-family: 'fontFamily.sans', ui-sans-serif, system-ui, -apple-system,
			BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',
			'Segoe UI Symbol', 'Noto Color Emoji';
	"
>
	<div style="width: 100%">
		<div
			style="
				width: 370px;
				margin: auto;
				background: #ffffff;
				padding: 20px;
				margin-bottom: 20px;
				border-radius: 4px;
				box-shadow: 0 4px 6px -1px #00000020;
			"
		>
			<div style="width: 100%; margin-bottom: 28px">
				<p
					style="
						width: 100%;
						text-align: center;
						margin: 0px;
						margin-bottom: 12px;
						font-size: 20px;
						line-height: 28px;
						font-weight: 600;
					"
				>
					Activar usuario
				</p>

				<p
					style="
						width: 100%;
						text-align: center;
						font-size: 14px;
						line-height: 20px;
					"
				>
					Bienvenido a la plataforma de fruitexco, este es el ultimo
					paso para activar su cuenta. Por favor haga clic en el botón
					para activar su cuenta
				</p>
			</div>

			<a href="[URL]" target="_blank" style="text-decoration: none">
				<div
					style="
						width: 100%;
						padding-top: 10px;
						padding-bottom: 10px;
						border-radius: 4px;
						box-shadow: 0 4px 6px -1px #00000020;
						background-color: #15803d;
					"
				>
					<p
						style="
							width: 100%;
							text-align: center;
							color: #ffffff;
							font-weight: 600;
							text-decoration: none;
							margin: 0%;
						"
					>
						Activar cuenta
					</p>
				</div>
			</a>

			<p
				style="
					width: 100%;
					text-align: center;
					font-size: 14px;
					line-height: 20px;
				"
			>
				La posibilidad de activar la cuenta vencerá en 15 minutos
			</p>
		</div>
	</div>
</body>
"""
        file_content = file_content.replace('[URL]', self.url)
        return file_content


class RecoverEmail(Email):
    def create_mail(self) -> str:
        file_content = """<body style="
		background-color: #eeeeee;
		padding: 5%;
		font-family: 'fontFamily.sans', ui-sans-serif, system-ui, -apple-system,
			BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',
			'Segoe UI Symbol', 'Noto Color Emoji';
	">
	<div style="width: 100%">
		<div style="
				width: 370px;
				margin: auto;
				background: #ffffff;
				padding: 20px;
				margin-bottom: 20px;
				border-radius: 4px;
				box-shadow: 0 4px 6px -1px #00000020;
			">
			<div style="width: 100%; margin-bottom: 28px">
				<p style="
						width: 100%;
						text-align: center;
						margin: 0px;
						margin-bottom: 12px;
						font-size: 20px;
						line-height: 28px;
						font-weight: 600;
					">
					Recuperar usuario
				</p>

				<p style="
						width: 100%;
						text-align: center;
						font-size: 14px;
						line-height: 20px;
					">
					Este correo sirve para reucerpar su cuenta, por favor de clic al siguiente botón e ingrese la nueva
					contraseña
				</p>
			</div>

			<a href="[URL]" target="_blank" style="text-decoration: none">
				<div style="
						width: 100%;
						padding-top: 10px;
						padding-bottom: 10px;
						border-radius: 4px;
						box-shadow: 0 4px 6px -1px #00000020;
						background-color: #15803d;
					">
					<p style="
							width: 100%;
							text-align: center;
							color: #ffffff;
							font-weight: 600;
							text-decoration: none;
							margin: 0%;
						">
						Recuperar cuenta
					</p>
				</div>
			</a>

			<p style="
					width: 100%;
					text-align: center;
					font-size: 14px;
					line-height: 20px;
				">
				La posibilidad de recueperar la cuenta vencerá en 15 minutos
			</p>
		</div>
	</div>
</body>"""
        file_content = file_content.replace('[URL]', self.url)
        return file_content

class ChangePassword(Email):
    def create_mail(self) -> str:
        file_content = """<body style="
		background-color: #eeeeee;
		padding: 5%;
		font-family: 'fontFamily.sans', ui-sans-serif, system-ui, -apple-system,
			BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',
			'Segoe UI Symbol', 'Noto Color Emoji';
	">
	<div style="width: 100%">
		<div style="
				width: 370px;
				margin: auto;
				background: #ffffff;
				padding: 20px;
				margin-bottom: 20px;
				border-radius: 4px;
				box-shadow: 0 4px 6px -1px #00000020;
			">
			<div style="width: 100%; margin-bottom: 28px">
				<p style="
						width: 100%;
						text-align: center;
						margin: 0px;
						margin-bottom: 12px;
						font-size: 20px;
						line-height: 28px;
						font-weight: 600;
					">
					Cambiar contraseña
				</p>

				<p style="
						width: 100%;
						text-align: center;
						font-size: 14px;
						line-height: 20px;
					">
					Alguien esta intentando acceder a su cuenta sin permiso.
					Este correo le da la posibilidad de cambiar su contraseña, si lo considera necesario.
				</p>
			</div>

			<a href="[URL]" target="_blank" style="text-decoration: none">
				<div style="
						width: 100%;
						padding-top: 10px;
						padding-bottom: 10px;
						border-radius: 4px;
						box-shadow: 0 4px 6px -1px #00000020;
						background-color: #15803d;
					">
					<p style="
							width: 100%;
							text-align: center;
							color: #ffffff;
							font-weight: 600;
							text-decoration: none;
							margin: 0%;
						">
						Cambiar contraseña
					</p>
				</div>
			</a>

			<p style="
					width: 100%;
					text-align: center;
					font-size: 14px;
					line-height: 20px;
				">
				La posibilidad de cambiar la contraseña vencerá en 15 minutos
			</p>
		</div>
	</div>
</body>"""
        file_content = file_content.replace('[URL]', self.url)
        return file_content