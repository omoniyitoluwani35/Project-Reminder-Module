from odoo import models, fields, api
from datetime import timedelta, datetime


class ProjectProject(models.Model):
    _inherit = 'project.project'

    reminder_frequency = fields.Selection([
        ('minutes', 'Minutes'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ], string="Reminder Frequency", default='daily')
    last_reminder_date = fields.Datetime("Last reminder Date")






    @api.model
    def send_reminders(self):
        projects = self.search([('reminder_frequency', '!=', False)])
        for project in projects:
            next_reminder_date = {
                'minutes': timedelta(minutes=4),
                'daily': timedelta(days=1),
                'weekly': timedelta(weeks=1),
                'bi_weekly': timedelta(weeks=2),
                'quarterly': timedelta(days=90),
                'annually': timedelta(days=365),
            }[project.reminder_frequency]

            last_reminder = project.last_reminder_date or project.create_date

            if last_reminder and project.last_update_id.create_date:
                last_reminder = max(last_reminder,project.last_update_id.create_date)
            else:
                last_reminder = last_reminder or project.last_update_id.create_date

            # Check if reminder needs to be sent
            if last_reminder + next_reminder_date <= datetime.now():
                # Create an activity in the chatter
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'res_id': project.id,
                    'res_model_id': self.env['ir.model']._get('project.project').id,
                    'summary': 'Provide a project update',
                    'user_id': project.user_id.id,
                })
                project.last_reminder_date = fields.Datetime.now()

