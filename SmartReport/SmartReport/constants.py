"""
Single source of truth for ALL permission codenames.
Import from here everywhere. Never type raw strings in views.

Rule: in views typing 'report.submit' in a view then the wrong way of doing,
instead do Import ReportPermissions.SUBMIT instead.
"""

class ReportPermissions():
    SUBMIT = 'report.submit'
    VIEW_OWN = 'report.view_own'
    VIEW_PROVINCE = 'report.view_province'
    VIEW_ALL = 'report.view_all'
    REVIEW = 'report.review'
    ESCALATE = 'report.escalate'
    DELETE = 'report.delete'
    CLOSE = 'report.close'
    CHANGE_PRIORITY = 'report.change_priority'
    MERGE_CLUSTER = 'report.merge_cluster'     #duplicate detect

class UserPermissions():
    VIEW_ALL = 'report.view_all'
    PROMOTE_STAFF = 'report.promote_to_staff'
    DEACTIVATE = 'report.deactivate'
    VERIFY_STAFF = 'report.verify'

class DashboardPermissions():
    VIEW_PROVINCE = 'report.view_province'
    VIEW_NATIONAL = 'report.view_national'
    EXPORT_DATA = 'report.export_data'


class RegionPermissions:
    VIEW             = 'region.view'
    MANAGE           = 'region.manage'

# ── Master permission list ─────────────────────────────────
# (codename, resource, description)
ALL_PERMISSIONS = [
    # Reports
    (ReportPermissions.SUBMIT,          'report',    'Submit a new road issue report'),
    (ReportPermissions.VIEW_OWN,        'report',    'View own submitted reports'),
    (ReportPermissions.VIEW_PROVINCE,   'report',    'View all reports in assigned province'),
    (ReportPermissions.VIEW_ALL,        'report',    'View all reports across Nepal'),
    (ReportPermissions.REVIEW,          'report',    'Review and update report status'),
    (ReportPermissions.ESCALATE,        'report',    'Escalate report to national level'),
    (ReportPermissions.DELETE,          'report',    'Delete a report'),
    (ReportPermissions.CLOSE,           'report',    'Mark report as resolved'),
    (ReportPermissions.CHANGE_PRIORITY, 'report',    'Override auto-calculated priority score'),
    (ReportPermissions.MERGE_CLUSTER,   'report',    'Merge duplicate reports into one cluster'),
    # Users
    (UserPermissions.VIEW_ALL,          'user',      'View all registered users'),
    (UserPermissions.PROMOTE_STAFF,     'user',      'Promote citizen to province staff'),
    (UserPermissions.DEACTIVATE,        'user',      'Deactivate a user account'),
    (UserPermissions.VERIFY_STAFF,      'user',      'Verify staff identity and credentials'),
    # Dashboard
    (DashboardPermissions.VIEW_PROVINCE,'dashboard', 'View province-level statistics'),
    (DashboardPermissions.VIEW_NATIONAL,'dashboard', 'View national statistics'),
    (DashboardPermissions.EXPORT_DATA,  'dashboard', 'Export report data as CSV/PDF'),
    # Regions
    (RegionPermissions.VIEW,            'region',    'View province and district data'),
    (RegionPermissions.MANAGE,          'region',    'Add or update region data'),
]


# ── Role → Permission mapping ──────────────────────────────
# Change permissions here and re-seed — zero code change needed.
ROLE_PERMISSION_MAP = {
    'citizen': [
        ReportPermissions.SUBMIT,
        ReportPermissions.VIEW_OWN,
        RegionPermissions.VIEW,
    ],
    'province_staff': [
        ReportPermissions.SUBMIT,
        ReportPermissions.VIEW_OWN,
        ReportPermissions.VIEW_PROVINCE,
        ReportPermissions.REVIEW,
        ReportPermissions.ESCALATE,
        ReportPermissions.CLOSE,
        ReportPermissions.MERGE_CLUSTER,
        RegionPermissions.VIEW,
        DashboardPermissions.VIEW_PROVINCE,
    ],
    'province_manager': [
        ReportPermissions.SUBMIT,
        ReportPermissions.VIEW_OWN,
        ReportPermissions.VIEW_PROVINCE,
        ReportPermissions.REVIEW,
        ReportPermissions.ESCALATE,
        ReportPermissions.DELETE,
        ReportPermissions.CLOSE,
        ReportPermissions.CHANGE_PRIORITY,
        ReportPermissions.MERGE_CLUSTER,
        UserPermissions.VIEW_ALL,
        UserPermissions.PROMOTE_STAFF,
        UserPermissions.VERIFY_STAFF,
        RegionPermissions.VIEW,
        DashboardPermissions.VIEW_PROVINCE,
        DashboardPermissions.EXPORT_DATA,
    ],
    'national_admin': [
        '__all__'   # every permission — resolved dynamically in seed
    ],
}