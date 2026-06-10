"""
Single source of truth for ALL permission codenames.
Import from here everywhere. Never type raw strings in views.
"""

class ReportPermissions:
    SUBMIT = 'report.submit'
    VIEW_OWN = 'report.view_own'
    VIEW_REGION = 'report.view_region'
    VIEW_ALL = 'report.view_all'
    UPDATE_STATUS = 'report.update_status'
    ASSIGN = 'report.assign'
    DELETE = 'report.delete'
    VERIFY_RESOLVED = 'report.verify_resolved'
    CHANGE_PRIORITY = 'report.change_priority'
    MERGE_CLUSTER = 'report.merge_cluster'

class UserPermissions:
    MANAGE_REGION = 'user.manage_region'
    MANAGE_ALL = 'user.manage_all'

class RegionPermissions:
    MANAGE = 'region.manage'

# ── Master permission list ─────────────────────────────────
# (codename, resource, description)
ALL_PERMISSIONS = [
    (ReportPermissions.SUBMIT,          'report', 'Submit a new road issue report'),
    (ReportPermissions.VIEW_OWN,        'report', 'View own submitted reports'),
    (ReportPermissions.VIEW_REGION,     'report', 'View reports in assigned region'),
    (ReportPermissions.VIEW_ALL,        'report', 'View all reports across Nepal'),
    (ReportPermissions.UPDATE_STATUS,   'report', 'Update status of a report'),
    (ReportPermissions.ASSIGN,          'report', 'Assign report to staff'),
    (ReportPermissions.DELETE,          'report', 'Delete a report'),
    (ReportPermissions.VERIFY_RESOLVED, 'report', 'Verify a report is resolved'),
    (ReportPermissions.CHANGE_PRIORITY, 'report', 'Override auto-calculated priority score'),
    (ReportPermissions.MERGE_CLUSTER,   'report', 'Merge duplicate reports into one cluster'),
    (UserPermissions.MANAGE_REGION,     'user',   'Manage users in region'),
    (UserPermissions.MANAGE_ALL,        'user',   'Manage all users'),
    (RegionPermissions.MANAGE,          'region', 'Manage regions'),
]

ROLE_PORTAL_MAP = {
    'citizen':            'citizen',
    'ward_staff':         'ward',
    'district_admin':     'district',
    'national_admin':     'admin',
}

# ── Role → Permission mapping ──────────────────────────────
ROLE_PERMISSION_MAP = {
    'citizen': [
        ReportPermissions.SUBMIT,
        ReportPermissions.VIEW_OWN,
        ReportPermissions.VIEW_REGION,
        ReportPermissions.UPDATE_STATUS,
        ReportPermissions.VERIFY_RESOLVED,
    ],
    'ward_staff': [
        ReportPermissions.SUBMIT,
        ReportPermissions.VIEW_OWN,
        ReportPermissions.VIEW_REGION,
        ReportPermissions.UPDATE_STATUS,
    ],
    'district_admin': [
        ReportPermissions.SUBMIT,
        ReportPermissions.VIEW_OWN,
        ReportPermissions.VIEW_REGION,
        ReportPermissions.UPDATE_STATUS,
        ReportPermissions.ASSIGN,
        ReportPermissions.VERIFY_RESOLVED,
        ReportPermissions.CHANGE_PRIORITY,
        ReportPermissions.MERGE_CLUSTER,
        UserPermissions.MANAGE_REGION,
    ],
    'national_admin': [
        '__all__'
    ],
}