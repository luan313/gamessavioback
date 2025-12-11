class EmailTemplates:
    def _base_template(self, title: str, content: str) -> str:
        """
            Template base para todos os emails.
        """
        bg_color = "#0f172a"
        card_bg = "#1e293b" 
        text_color = "#f8fafc" 

        return f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>
                    /* Reset styles */
                    body {{ margin: 0; padding: 0; min-width: 100%; width: 100% !important; height: 100% !important; }}
                    body, table, td, div, p, a {{ -webkit-font-smoothing: antialiased; text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; line-height: 100%; }}
                    table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse !important; border-spacing: 0; }}
                    img {{ border: 0; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }}
                    
                    /* Responsive styles */
                    @media screen and (max-width: 600px) {{
                        .email-container {{ width: 100% !important; max-width: 100% !important; }}
                        .fluid-img {{ height: auto !important; max-width: 100% !important; width: 100% !important; }}
                        .padding-mobile {{ padding: 15px !important; }}
                        .text-mobile {{ font-size: 14px !important; }}
                        .header-mobile {{ font-size: 20px !important; }}
                        .price-mobile {{ font-size: 28px !important; }}
                        .cta-button {{ display: block !important; width: 100% !important; box-sizing: border-box !important; text-align: center !important; }}
                    }}
                </style>
            </head>
            <body style="margin: 0; padding: 0; background-color: {bg_color}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: {text_color};">
                <center style="width: 100%; background-color: {bg_color};">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: {bg_color}; width: 100%; margin: 0 auto;">
                        <tr>
                            <td align="center" style="padding: 20px 10px;">
                                <!-- Main Container -->
                                <table role="presentation" class="email-container" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: {card_bg}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); width: 100%; max-width: 600px; margin: 0 auto;">
                                    {content}
                                    
                                    <!-- Footer -->
                                    <tr>
                                        <td style="padding: 15px; background-color: #0f172a; text-align: center; border-top: 1px solid #334155;">
                                            <p style="margin: 0; font-size: 11px; color: #64748b;">
                                                &copy; 2024 GamesSavio.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </center>
            </body>
            </html>
        """


    def _get_html_template_games_notification(self, user_name: str, game_name: str, current_price: float, target_price: float, deal_url: str, image_url: str | None) -> str:
        """
            Gera um template HTML para notificação de preço baixado.
        """
        primary_color = "#7c3aed" 
        text_color = "#f8fafc" 
        accent_color = "#10b981" 

        content = f"""
            <!-- Image Section -->
            <tr>
                <td style="padding: 0; background-color: #000; text-align: center;">
                    {f'<img src="{image_url}" alt="{game_name}" class="fluid-img" style="width: 100%; height: auto; display: block; max-height: 200px; object-fit: cover; border: 0;">' if image_url else ''}
                </td>
            </tr>

            <!-- Content Section -->
            <tr>
                <td class="padding-mobile" style="padding: 25px 20px;">
                    <h1 class="header-mobile" style="margin: 0 0 15px 0; font-size: 22px; color: {text_color}; text-align: center;">Preço Atingido! 🎯</h1>
                    
                    <p class="text-mobile" style="margin: 0 0 15px 0; font-size: 15px; line-height: 1.5; color: #cbd5e1;">
                        Olá <strong>{user_name}</strong>, o jogo <strong>{game_name}</strong> atingiu seu preço alvo.
                    </p>

                    <!-- Price Box -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 20px;">
                        <tr>
                            <td style="padding: 15px; text-align: center;">
                                <p style="margin: 0 0 5px 0; font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Preço Atual</p>
                                <p class="price-mobile" style="margin: 0; font-size: 32px; font-weight: bold; color: {accent_color};">R$ {current_price:.2f}</p>
                                <p style="margin: 5px 0 0 0; font-size: 13px; color: #94a3b8;">Seu alvo: R$ {target_price:.2f}</p>
                            </td>
                        </tr>
                    </table>

                    <!-- CTA Button -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                        <tr>
                            <td align="center">
                                <a href="{deal_url}" class="cta-button" style="display: inline-block; padding: 14px 28px; background-color: {primary_color}; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px; transition: background-color 0.3s; width: auto; min-width: 180px; text-align: center;">
                                    Ver Oferta
                                </a>
                            </td>
                        </tr>
                    </table>
                    
                    <p style="margin: 20px 0 0 0; font-size: 12px; color: #64748b; text-align: center; line-height: 1.4;">
                        *Verifique a loja para confirmar.
                    </p>
                </td>
            </tr>
        """
        return self._base_template("Alerta de Preço - GamesSavio", content)
       

    def prepare_content_games_notification(self, user_name: str, game_name: str, current_price: float, target_price: float, deal_url: str, image_url: str | None) -> str:
        """Helper para preparar o conteúdo HTML específico de email"""
        return self._get_html_template_games_notification(user_name, game_name, current_price, target_price, deal_url, image_url)


    def _get_html_template_password_recovery(self, user_name: str, reset_url: str) -> str:
        """
            Gera um template HTML para recuperação de senha.
        """
        primary_color = "#7c3aed" 
        card_bg = "#1e293b" 
        text_color = "#f8fafc" 

        content = f"""
            <!-- Header Section -->
            <tr>
                <td style="padding: 30px 20px; text-align: center; background-color: {card_bg}; border-bottom: 1px solid #334155;">
                    <h1 class="header-mobile" style="margin: 0; font-size: 24px; color: {text_color};">GamesSavio</h1>
                </td>
            </tr>

            <!-- Content Section -->
            <tr>
                <td class="padding-mobile" style="padding: 40px 30px;">
                    <h2 class="header-mobile" style="margin: 0 0 20px 0; font-size: 22px; color: {text_color}; text-align: center;">Recuperação de Senha 🔒</h2>
                    
                    <p class="text-mobile" style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #cbd5e1; text-align: center;">
                        Olá <strong>{user_name}</strong>,<br><br>
                        Recebemos uma solicitação para redefinir a senha da sua conta. Se você não fez essa solicitação, pode ignorar este email com segurança.
                    </p>

                    <!-- CTA Button -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 30px 0;">
                        <tr>
                            <td align="center">
                                <a href="{reset_url}" class="cta-button" style="display: inline-block; padding: 14px 28px; background-color: {primary_color}; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; transition: background-color 0.3s; width: auto; min-width: 200px; text-align: center;">
                                    Redefinir Senha
                                </a>
                            </td>
                        </tr>
                    </table>
                    
                    <p style="margin: 20px 0 0 0; font-size: 13px; color: #94a3b8; text-align: center; line-height: 1.5;">
                        Este link expira em 30 minutos.<br>
                        Se o botão não funcionar, copie e cole o link abaixo no seu navegador:<br>
                        <span style="color: {primary_color}; word-break: break-all;">{reset_url}</span>
                    </p>
                </td>
            </tr>
        """
        return self._base_template("Recuperação de Senha - GamesSavio", content)


    def prepare_content_password_recovery(self, user_name: str, reset_url: str) -> str:
        """Helper para preparar o conteúdo HTML de recuperação de senha"""
        return self._get_html_template_password_recovery(user_name, reset_url)


    def _get_html_template_email_validation(self, user_name: str, validation_url: str) -> str:
        """
            Gera um template HTML para validação de email.
        """
        primary_color = "#7c3aed" 
        card_bg = "#1e293b" 
        text_color = "#f8fafc" 

        content = f"""
            <!-- Header Section -->
            <tr>
                <td style="padding: 30px 20px; text-align: center; background-color: {card_bg}; border-bottom: 1px solid #334155;">
                    <h1 class="header-mobile" style="margin: 0; font-size: 24px; color: {text_color};">GamesSavio</h1>
                </td>
            </tr>

            <!-- Content Section -->
            <tr>
                <td class="padding-mobile" style="padding: 40px 30px;">
                    <h2 class="header-mobile" style="margin: 0 0 20px 0; font-size: 22px; color: {text_color}; text-align: center;">Bem-vindo(a)! 👋</h2>
                    
                    <p class="text-mobile" style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #cbd5e1; text-align: center;">
                        Olá <strong>{user_name}</strong>,<br><br>
                        Obrigado por se cadastrar no GamesSavio. Para ativar sua conta e começar a monitorar seus jogos favoritos, por favor confirme seu endereço de email.
                    </p>

                    <!-- CTA Button -->
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 30px 0;">
                        <tr>
                            <td align="center">
                                <a href="{validation_url}" class="cta-button" style="display: inline-block; padding: 14px 28px; background-color: {primary_color}; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; transition: background-color 0.3s; width: auto; min-width: 200px; text-align: center;">
                                    Confirmar Email
                                </a>
                            </td>
                        </tr>
                    </table>
                    
                    <p style="margin: 20px 0 0 0; font-size: 13px; color: #94a3b8; text-align: center; line-height: 1.5;">
                        Se o botão não funcionar, copie e cole o link abaixo no seu navegador:<br>
                        <span style="color: {primary_color}; word-break: break-all;">{validation_url}</span>
                    </p>
                </td>
            </tr>
        """
        return self._base_template("Confirmação de Email - GamesSavio", content)


    def prepare_content_email_validation(self, user_name: str, validation_url: str) -> str:
        """Helper para preparar o conteúdo HTML de validação de email"""
        return self._get_html_template_email_validation(user_name, validation_url)


email_templates = EmailTemplates()


    