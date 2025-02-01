{
    'name': 'Project Update Reminder',
    'version': '1.0',
    'summary': 'Send reminders to project managers for project updates.',
    'category': 'Project',
    'author': 'Tolu',
    'depends': ['project', 'mail'],
    'data': [
        'data/ir_cron_data.xml',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}