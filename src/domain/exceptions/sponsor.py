class SponsorError(Exception):
    pass


class SponsorAlreadyExistsError(SponsorError):
    pass


class SponsorAccessDeniedError(SponsorError):
    pass


class SponsorInvalidExpireDateError(SponsorError):
    pass
