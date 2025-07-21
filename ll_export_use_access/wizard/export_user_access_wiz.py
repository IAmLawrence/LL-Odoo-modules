import base64
import io
from odoo import models, fields, api
import xlsxwriter


class LLExportUserAccess(models.TransientModel):
    _name = 'll.export.user.access'
    _description = 'Export User Access Report'

    file_data = fields.Binary('File', readonly=True)
    file_name = fields.Char('Filename', default='user_access_rights.xlsx')

    def export_user_access_excel(self):
        Users = self.env['res.users'].search([])
        Groups = self.env['res.groups'].search([])

        app_groups = {}
        for group in Groups:
            parts = group.full_name.split('/')
            if len(parts) >= 2:
                app = parts[0].strip()
                grp = parts[1].strip()
                app_groups.setdefault(app, []).append((grp, group))

        user_app_group = {}
        for user in Users:
            mapping = {}
            for group in user.groups_id:
                parts = group.full_name.split('/')
                if len(parts) >= 2:
                    app = parts[0].strip()
                    grp = parts[1].strip()
                    mapping[app] = grp
            user_app_group[user.login] = mapping

        sorted_user_items = sorted(user_app_group.items(), key=lambda item: item[0].lower())

        apps = sorted(app_groups.keys())

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        bold = workbook.add_format({'bold': True})

        ws1 = workbook.add_worksheet("User Groups")
        ws1.write(0, 0, 'User', bold)
        for col, app in enumerate(apps, start=1):
            ws1.write(0, col, app, bold)

        for row, (user, mapping) in enumerate(sorted_user_items, start=1):
            ws1.write(row, 0, user)
            for col, app in enumerate(apps, start=1):
                ws1.write(row, col, mapping.get(app, ''))

        workbook.close()
        output.seek(0)

        self.file_data = base64.b64encode(output.read())
        self.file_name = 'user_access_rights.xlsx'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
