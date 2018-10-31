import datetime
import warnings as _warnings
from enum import Enum

from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_PERSISTENT
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS
from saml2.saml import NAMEID_FORMAT_UNSPECIFIED

from satosa.internal import InternalData
from satosa import util


_warnings.simplefilter("default")


class _DeprecatedInternalData(InternalData):
    def __init__(
        self,
        auth_info=None,
        requester=None,
        requester_name=None,
        subject_id=None,
        subject_type=None,
        attributes=None,
        user_id=None,
        user_id_hash_type=None,
        name_id=None,
        approved_attributes=None,
    ):
        return super().__init__(
            auth_info=auth_info,
            requester=requester,
            requester_name=requester_name,
            subject_id=subject_id or user_id or name_id,
            subject_type=subject_type or user_id_hash_type,
            attributes=attributes,
        )

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "user_id": self.subject_id,
                "user_id_hash_type": self.subject_type,
                "name_id": self.subject_id,
                "approved_attributes": self.attributes,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data):
        instance = InternalData.from_dict(data)
        instance.attributes = data.get("attributes") or data.get(
            "approved_attributes"
        )
        instance.subject_type = data.get("subject_type") or data.get(
            "user_id_hash_type"
        )
        instance.subject_id = (
            data.get("subject_id")
            or data.get("user_id")
            or data.get("name_id")
        )
        return instance

    @property
    def user_id(self):
        msg = "user_id is deprecated; use subject_id instead."
        _warnings.warn(msg, DeprecationWarning)
        return self.subject_id

    @user_id.setter
    def user_id(self, value):
        msg = "user_id is deprecated; use subject_id instead."
        _warnings.warn(msg, DeprecationWarning)
        self.subject_id = value

    @property
    def user_id_hash_type(self):
        msg = "user_id_hash_type is deprecated; use subject_type instead."
        _warnings.warn(msg, DeprecationWarning)
        return self.subject_type

    @user_id_hash_type.setter
    def user_id_hash_type(self, value):
        msg = "user_id_hash_type is deprecated; use subject_type instead."
        _warnings.warn(msg, DeprecationWarning)
        self.subject_type = value

    @property
    def approved_attributes(self):
        msg = "approved_attributes is deprecated; use attributes instead."
        _warnings.warn(msg, DeprecationWarning)
        return self.attributes

    @approved_attributes.setter
    def approved_attributes(self, value):
        msg = "approved_attributes is deprecated; use attributes instead."
        _warnings.warn(msg, DeprecationWarning)
        self.attributes = value

    @property
    def name_id(self):
        msg = "name_id is deprecated; use subject_id instead."
        _warnings.warn(msg, DeprecationWarning)
        return self.subject_id

    @name_id.setter
    def name_id(self, value):
        msg = "name_id is deprecated; use subject_id instead."
        _warnings.warn(msg, DeprecationWarning)
        self.subject_id = value


class InternalRequest(_DeprecatedInternalData):
    def __init__(self, user_id_hash_type, requester, requester_name=None):
        msg = (
            "InternalRequest is deprecated."
            " Use satosa.internal.InternalData class instead."
        )
        _warnings.warn(msg, DeprecationWarning)
        super().__init__(
            user_id_hash_type=user_id_hash_type,
            requester=requester,
            requester_name=requester_name,
        )


class InternalResponse(_DeprecatedInternalData):
    def __init__(self, auth_info=None):
        msg = (
            "InternalResponse is deprecated."
            " Use satosa.internal.InternalData class instead."
        )
        _warnings.warn(msg, DeprecationWarning)
        super().__init__(auth_info=auth_info)


class SAMLInternalResponse(InternalResponse):
    """
    Like the parent InternalResponse, holds internal representation of
    service related data, but includes additional details relevant to
    SAML interoperability.

    :type name_id: instance of saml2.saml.NameID from pysaml2
    """

    def __init__(self, auth_info=None):
        msg = (
            "SAMLInternalResponse is deprecated."
            " Use satosa.internal.InternalData class instead."
        )
        _warnings.warn(msg, DeprecationWarning)
        super().__init__(auth_info=auth_info)


class UserIdHashType(Enum):
    """
    All different user id hash types
    """

    transient = 1
    persistent = 2
    pairwise = 3
    public = 4
    emailaddress = 5
    unspecified = 6

    def __getattr__(self, name):
        msg = "UserIdHashType is deprecated and will be removed."
        _warnings.warn(msg, DeprecationWarning)
        return self.__getattribute__(name)

    @classmethod
    def from_string(cls, str):
        msg = "UserIdHashType is deprecated and will be removed."
        _warnings.warn(msg, DeprecationWarning)
        try:
            return getattr(cls, str)
        except AttributeError:
            raise ValueError("Unknown hash type '{}'".format(str))


class UserIdHasher(object):
    """
    Class for creating different user id types
    """

    STATE_KEY = "IDHASHER"

    @staticmethod
    def save_state(internal_request, state):
        """
        Saves all necessary information needed by the UserIdHasher

        :type internal_request: satosa.internal_data.InternalRequest

        :param internal_request: The request
        :param state: The current state
        """
        state_data = {"hash_type": internal_request.user_id_hash_type}
        state[UserIdHasher.STATE_KEY] = state_data

    @staticmethod
    def hash_data(salt, value):
        """
        Hashes a value together with a salt.
        :type salt: str
        :type value: str
        :param salt: hash salt
        :param value: value to hash together with the salt
        :return: hash value (SHA512)
        """
        msg = "UserIdHasher is deprecated; use satosa.util.hash_data instead."
        _warnings.warn(msg, DeprecationWarning)
        return util.hash_data(salt, value)

    @staticmethod
    def hash_type(state):
        state_data = state[UserIdHasher.STATE_KEY]
        hash_type = state_data["hash_type"]
        return hash_type

    @staticmethod
    def hash_id(salt, user_id, requester, state):
        """
        Sets a user id to the internal_response,
        in the format specified by the internal response

        :type salt: str
        :type user_id: str
        :type requester: str
        :type state: satosa.state.State
        :rtype: str

        :param salt: A salt string for the ID hashing
        :param user_id: the user id
        :param user_id_hash_type: Hashing type
        :param state: The current state
        :return: the internal_response containing the hashed user ID
        """
        hash_type_to_format = {
            NAMEID_FORMAT_TRANSIENT: "{id}{req}{time}",
            NAMEID_FORMAT_PERSISTENT: "{id}{req}",
            "pairwise": "{id}{req}",
            "public": "{id}",
            NAMEID_FORMAT_EMAILADDRESS: "{id}",
            NAMEID_FORMAT_UNSPECIFIED: "{id}",
        }

        format_args = {
            "id": user_id,
            "req": requester,
            "time": datetime.datetime.utcnow().timestamp(),
        }

        hash_type = UserIdHasher.hash_type(state)
        try:
            fmt = hash_type_to_format[hash_type]
        except KeyError as e:
            raise ValueError("Unknown hash type: {}".format(hash_type)) from e
        else:
            user_id = fmt.format(**format_args)

        hasher = (
            (lambda salt, value: value)
            if hash_type
            in [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED]
            else util.hash_data
        )
        return hasher(salt, user_id)


def saml_name_id_format_to_hash_type(name_format):
    """
    Translate pySAML2 name format to satosa format

    :type name_format: str
    :rtype: satosa.internal_data.UserIdHashType
    :param name_format: SAML2 name format
    :return: satosa format
    """
    msg = "saml_name_id_format_to_hash_type is deprecated and will be removed."
    _warnings.warn(msg, DeprecationWarning)

    name_id_format_to_hash_type = {
        NAMEID_FORMAT_TRANSIENT: UserIdHashType.transient,
        NAMEID_FORMAT_PERSISTENT: UserIdHashType.persistent,
        NAMEID_FORMAT_EMAILADDRESS: UserIdHashType.emailaddress,
        NAMEID_FORMAT_UNSPECIFIED: UserIdHashType.unspecified,
    }

    return name_id_format_to_hash_type.get(
        name_format, UserIdHashType.transient
    )


def hash_type_to_saml_name_id_format(hash_type):
    """
    Translate satosa format to pySAML2 name format

    :type hash_type: satosa.internal_data.UserIdHashType
    :rtype: str
    :param hash_type: satosa format
    :return: pySAML2 name format
    """
    msg = "hash_type_to_saml_name_id_format is deprecated and will be removed."
    _warnings.warn(msg, DeprecationWarning)

    hash_type_to_name_id_format = {
        UserIdHashType.transient: NAMEID_FORMAT_TRANSIENT,
        UserIdHashType.persistent: NAMEID_FORMAT_PERSISTENT,
        UserIdHashType.emailaddress: NAMEID_FORMAT_EMAILADDRESS,
        UserIdHashType.unspecified: NAMEID_FORMAT_UNSPECIFIED,
    }

    return hash_type_to_name_id_format.get(hash_type, NAMEID_FORMAT_PERSISTENT)


def oidc_subject_type_to_hash_type(subject_type):
    msg = "oidc_subject_type_to_hash_type is deprecated and will be removed."
    _warnings.warn(msg, DeprecationWarning)

    if subject_type == "public":
        return UserIdHashType.public

    return UserIdHashType.pairwise


def hash_attributes(hash_attributes, internal_attributes, salt):
    # Hash all attributes specified in INTERNAL_ATTRIBUTES["hash"]
    for attribute in hash_attributes:
        msg = (
            "'USER_ID_HASH_SALT' configuration option is deprecated."
            " 'hash' configuration option is deprecated."
            " Use the hasher microservice instead."
        )
        _warnings.warn(msg, DeprecationWarning)

        # hash all attribute values individually
        if attribute in internal_attributes:
            hashed_values = [
                util.hash_data(salt, v) for v in internal_attributes[attribute]
            ]
            internal_attributes[attribute] = hashed_values
