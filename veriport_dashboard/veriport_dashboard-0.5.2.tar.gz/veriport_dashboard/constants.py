from django.utils.translation import ugettext_lazy as _


ADULTERATED = 'ADU'
COMPLETED = 'COM'
NEGATIVE = 'NEG'
NEGATIVE_DILUTE = 'NDI'
NEGATIVE_TOR = 'NTR'
NEGATIVE_WITH_SAFETY_ADVISORY = 'NSA'
POSITIVE = 'POS'
POSITIVE_DILUTE = 'PDI'
PRELIMINARY_NEG = 'PNG'
REFUSAL_ADULTERATED = 'RAD'
REFUSAL_OTHER = 'ROT'
REFUSAL_SHY_BLADDER = 'RSB'
REFUSAL_SUBSTITUTED = 'RSB'
REJECTED_CANCELLED_NO_TEST = 'RCN'

MRO_VERIFICATION_CHOICES = (
    (ADULTERATED, _('Adulterated')),
    (COMPLETED, _('Completed')),
    (NEGATIVE, _('Negative')),
    (NEGATIVE_DILUTE, _('Negative dilute')),
    (NEGATIVE_TOR, _('Negative - Temperature out of range')),
    (NEGATIVE_WITH_SAFETY_ADVISORY, _('Negative with safety advisory')),
    (POSITIVE, _('Positive')),
    (POSITIVE_DILUTE, _('Positive dilute')),
    (PRELIMINARY_NEG, _('Preliminary negative')),
    (REFUSAL_ADULTERATED, _('Refusal - Adulterated')),
    (REFUSAL_OTHER, _('Refusal - Other')),
    (REFUSAL_SHY_BLADDER, _('Refusal - Shy bladder')),
    (REFUSAL_SUBSTITUTED, _('Refusal - Substituted')),
    (REJECTED_CANCELLED_NO_TEST, _('Rejected/Cancelled/No test')),
)

NOT_SPECIFIED = 'NS'
BLOOD = 'BL'
BREATH = 'BR'
HAIR = 'HR'
NAILS = 'NL'
ORAL_FLUID = 'OF'
SALIVA = 'SL'
SWEAT = 'SW'
URINE = 'UR'

SPECIMEN_TYPE_CHOICES = (
    (NOT_SPECIFIED, _('Not specified')),
    (BLOOD, _('Blood')),
    (BREATH, _('Breath')),
    (HAIR, _('Hair')),
    (NAILS, _('Nails')),
    (ORAL_FLUID, _('Oral Fluid, STT, Saliva')),
    (SALIVA, _('Saliva')),
    (SWEAT, _('Sweat')),
    (URINE, _('Urine')),
)

DURATION_LOOKUP = {
    "review": _("Review Duration"),
    "interview": _("Interview Duration"),
    "ccf": _("CCF Match Duration"),
    "dot": _("DOT Test Duration"),
    "non-dot": _("Non-DOT Duration"),
    "release": _("Release Duration"),
}

DURATION_FIELD_LOOKUP = {
    "review": "review_duration",
    "interview": "interview_duration",
    "ccf": "ccf_match_duration",
    "release": "release_report_duration",
}

REGULATED_ALL = "all"
REGULATED_DOT = "dot"
REGULATED_NONDOT = "non-dot"
REGULATED_TESTING_CHOICES = (
    (REGULATED_ALL, _("All")),
    (REGULATED_DOT, _("DOT")),
    (REGULATED_NONDOT, _("Non-DOT")),
)

TPA_LAST_MONTH = "all"
TPA_EMPLOYER = "employer"
TPA_CHOICES = (
    (TPA_LAST_MONTH, _("All Tests last Month")),
    (TPA_EMPLOYER, _("All Tests per Employer last Month")),
)

MRO_LAST_MONTH = "all"
MRO_EMPLOYER = "employer"
MRO_CHOICES = (
    (MRO_LAST_MONTH, _("All Tests last Month")),
    (MRO_EMPLOYER, _("All Tests per TPA last Month")),
)

ACCOUNT_ALL = "ALL"
COMPANY = 'COMP'
CONSORTIUM = 'CONS'
EMPLOYER = 'EMPL'
MRO = 'MRO'
TPA = 'TPA'
AGENCY = 'AGC'

ACCOUNT_TYPE_CHOICES = (
    (AGENCY, _('Agency')),
    (COMPANY, _('Company')),
    (CONSORTIUM, _('Consortium')),
    (EMPLOYER, _('Employer')),
    (MRO, _('MRO')),
    (TPA, _('TPA')),
)

FORM_ACCOUNT_TYPE_CHOICES = (
    ("all", _("All")),
    (AGENCY, _('Agency')),
    (COMPANY, _('Company')),
    (CONSORTIUM, _('Consortium')),
    (EMPLOYER, _('Employer')),
    (MRO, _('MRO')),
    (TPA, _('TPA')),
)
