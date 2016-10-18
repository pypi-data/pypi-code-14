# Copyright (c) 2015, Formation Data Systems, Inc. All Rights Reserved.
#

from base_cli_test import BaseCliTest
from model.common.named_credential import NamedCredential
from model.common.repository import Repository
from model.common.s3credentials import S3Credentials
from model.volume.volume import Volume
from model.admin.user import User
from model.admin.role import Role
from model.admin.tenant import Tenant
from model.volume.volume_status import VolumeStatus
from model.common.size import Size
from model.volume.exported_volume import ExportedVolume
from model.volume.settings.object_settings import ObjectSettings
from model.volume.qos_policy import QosPolicy
from model.volume.data_protection_policy import DataProtectionPolicy
from model.volume.safeguard_preset import SafeGuardPreset
from model.volume.snapshot_policy import SnapshotPolicy
from model.volume.subscription import Subscription
from model.volume.recurrence_rule import RecurrenceRule
from model.volume.remote_volume import RemoteVolume
from utils.converters.common.repository_converter import RepositoryConverter
from utils.converters.common.named_credential_converter import NamedCredentialConverter
from utils.converters.volume.preset_converter import PresetConverter
from utils.converters.volume.remote_volume_converter import RemoteVolumeConverter
from utils.converters.volume.subscription_converter import SubscriptionConverter
from utils.converters.volume.exported_volume_converter import ExportedVolumeConverter
from utils.converters.volume.volume_converter import VolumeConverter
from utils.converters.admin.user_converter import UserConverter
from utils.converters.admin.tenant_converter import TenantConverter
from model.platform.domain import Domain
from utils.converters.platform.domain_converter import DomainConverter
from model.platform.service import Service
from model.platform.service_status import ServiceStatus
from utils.converters.platform.service_converter import ServiceConverter
from model.platform.node import Node
from utils.converters.platform.node_converter import NodeConverter
from model.platform.address import Address

class TestConverters(BaseCliTest):
    '''
    Created on Jun 1, 2015
    
    @author: nate
    '''
    
    def test_volume_conversion(self):
        
        volume = Volume()
        volume.id = 34  
        volume.name = "TestVolume"
        volume.media_policy = "SSD"
        
        status = VolumeStatus()
        status.last_capacity_firebreak = 0
        status.last_performance_firebreak = 10000
        status.state = "AVAILABLE"
        status.current_usage = Size( 12, "TB" )
        volume.status = status
        volume.application = "MS Access"
        
        tenant = Tenant()
        tenant.id = 9
        tenant.name = "UNC"
        volume.tenant = tenant
        
        settings = ObjectSettings()
        settings.max_object_size = Size( 1, "GB" )
        volume.settings = settings
        
        qos_policy = QosPolicy()
        qos_policy.priority = 6
        qos_policy.iops_max = 5000
        qos_policy.iops_min = 3000
        volume.qos_policy = qos_policy
        
        p_policy = DataProtectionPolicy()
        p_policy.commit_log_retention = 86400
        p_policy.preset_id = None
        
        s_policy = SnapshotPolicy()
        s_policy.retention_time_in_seconds = 86400
        s_policy.preset_id = None
        
        rule = RecurrenceRule()
        rule.byday = "MO"
        rule.frequency = "WEEKLY"
        rule.byhour = 14
        rule.byminute = 45
        s_policy.recurrence_rule = rule
        
        p_policy.snapshot_policies = [s_policy]
        volume.data_protection_policy = p_policy 
        
        j_str = VolumeConverter.to_json(volume) 
        
        newVolume = VolumeConverter.build_volume_from_json(j_str)
        
        print j_str
        
        assert newVolume.name == "TestVolume"
        assert newVolume.id == 34
        assert newVolume.media_policy == "SSD"
        assert newVolume.status.state == "AVAILABLE"
        assert newVolume.status.last_capacity_firebreak == 0
        assert newVolume.status.last_performance_firebreak == 10000
        assert newVolume.status.current_usage.size == 12
        assert newVolume.status.current_usage.unit == "TB"
        assert newVolume.application == "MS Access"
        assert newVolume.qos_policy.priority == 6
        assert newVolume.qos_policy.iops_max == 5000
        assert newVolume.qos_policy.iops_min == 3000
        assert newVolume.data_protection_policy.commit_log_retention == 86400
        assert len(newVolume.data_protection_policy.snapshot_policies) == 1
        assert newVolume.tenant.id == 9
        assert newVolume.tenant.name == "UNC"
        
        new_s_policy = newVolume.data_protection_policy.snapshot_policies[0]
        
        assert new_s_policy.retention_time_in_seconds == 86400
        assert new_s_policy.recurrence_rule.frequency == "WEEKLY"
        assert new_s_policy.recurrence_rule.byday == "MO"
        assert new_s_policy.recurrence_rule.byhour == 14
        assert new_s_policy.recurrence_rule.byminute == 45
        
    def test_user_conversion(self):
        
        user = User()
        role = "USER"

        tenant = Tenant()
        tenant.name = "TheWorst"
        tenant.id = 2

        
        user.id = "5abc34"
        user.name = "jdoe"
        user.tenant = tenant
        user.role = role
        
        j_user = UserConverter.to_json(user)
        print j_user
        
        new_user = UserConverter.build_user_from_json(j_user)
        
        assert new_user.id == "5abc34"
        assert new_user.name == "jdoe"
        assert new_user.role == "USER"
        assert new_user.tenant.name == "TheWorst"
        assert new_user.tenant.id == 2
        
    def test_tenant_conversion(self):
        
        tenant = Tenant()
        
        tenant.id = 320
        tenant.name = "HisTenant"
        
        j_tenant = TenantConverter.to_json(tenant)
        print j_tenant
        
        new_tenant = TenantConverter.build_tenant_from_json(j_tenant)
        
        assert new_tenant.name == "HisTenant"
        assert new_tenant.id == 320
        
    def test_domain_conversion(self):
        
        domain = Domain()
        domain.site = "boulder"
        
        domain.id = 5102
        domain.name = "terrible.domain"
        
        j_domain = DomainConverter.to_json(domain)
        print j_domain
        
        new_domain = DomainConverter.build_domain_from_json(j_domain)
        
        assert new_domain.site == "boulder"
        assert new_domain.name == "terrible.domain"
        assert new_domain.id == 5102
        assert new_domain.state == Domain.STATE_UNKNOWN
        
    def test_service_conversion(self):
        
        service = Service()
        
        service.id = "qwerty"
        service.name = "AM"
        
        service.port = 7004
        service.type = "AM"
        
        status = ServiceStatus()
        status.state = "LIMITED"
        status.description = "Some fake description"
        status.error_code = 4001
        
        service.status = status
        
        j_service = ServiceConverter.to_json(service)
        print j_service
        
        new_service = ServiceConverter.build_service_from_json(j_service)
        
        assert new_service.id == "qwerty"
        assert new_service.name == "AM"
        assert new_service.type == "AM"
        
        new_status = new_service.status
        
        assert new_status.state == "LIMITED"
        assert new_status.description == "Some fake description"
        assert new_status.error_code == 4001

    def test_named_credential_conversion(self):

        # Mutual exclusion: s3 bucket versus remote volume.
        # First, try s3 bucket.
        s3credentials = S3Credentials()

        s3credentials.access_key_id = "AnAccessIdKey"
        s3credentials.secret_key = "ASecretKey"

        named_credential = NamedCredential()
        named_credential.digest = "aaaabbbb"
        named_credential.name = "goodcredential"
        named_credential.s3credentials = s3credentials
        named_credential.user_id = 42
        named_credential.url = "a/url"
        named_credential.bucketname = "tinpail"

        j_str = NamedCredentialConverter.to_json(named_credential)
        print j_str

        deserialized = NamedCredentialConverter.build_from_json(j_str)
        assert deserialized.digest == "aaaabbbb"
        assert deserialized.name == "goodcredential"
        assert deserialized.user_id == 42 
        assert deserialized.url == "a/url"
 
    def test_node_conversion(self):
        
        node  = Node()
        
        address = Address()
        
        address.ipv4address = "10.12.13.14"
        address.ipv6address = "someweirdaddress"
        node.address = address
        
        node.id = 928
        node.name = "CoolNode"
        
        node.state = "DOWN"
        
        service = Service()
        
        service.id = 21
        service.name = "DM"
        
        service.type = "DM"
        
        s_status = ServiceStatus()
        s_status.description = "Doing very medium"
        s_status.error_code = 201
        s_status.state = "DEGRADED"
        
        service.status = s_status
        
        node.services["DM"].append( service )
        
        j_node = NodeConverter.to_json(node)
        print j_node
        
        new_node = NodeConverter.build_node_from_json(j_node)
        
        assert new_node.address.ipv4address == "10.12.13.14"
        assert new_node.address.ipv6address == "someweirdaddress"
        assert new_node.id == 928
        assert new_node.name == "CoolNode"
        assert new_node.state == "DOWN"
        assert len(new_node.services["DM"]) == 1
        
        new_service = new_node.services["DM"][0]
        
        assert new_service.status.state == "DEGRADED"
        assert new_service.status.description == "Doing very medium"
        assert new_service.status.error_code == 201
        assert new_service.type == "DM"
        assert new_service.id == 21
        assert new_service.name == "DM"

    def test_repository_conversion(self):

        # Mutual exclusion: s3 bucket versus remote volume.
        # First, try s3 bucket.
        credentials = S3Credentials()

        credentials.access_key_id = "AnAccessIdKey"
        credentials.secret_key = "ASecretKey"

        repository = Repository()
        repository.uuid = "aaaabbbb"
        repository.credentials = credentials
        repository.volume_id = 42
        repository.url = "a/url"
        repository.bucket_name = "tinpail"
        repository.obj_prefix_key = "1/1/name"
        repository.new_volume_name = "newVolumeName"

        # These won't survive the round trip because s3 bucket is present
        repository.remote_om = "https://me:password@hostname:1234"
        repository.remote_volume_name = "volumeName"

        j_repo = RepositoryConverter.to_json(repository)
        print j_repo

        roundtrip_repo = RepositoryConverter.build_repository_from_json(j_repo)

        assert roundtrip_repo.uuid == "aaaabbbb"
        assert roundtrip_repo.credentials.access_key_id == "AnAccessIdKey"
        assert roundtrip_repo.credentials.secret_key == "ASecretKey"
        assert roundtrip_repo.volume_id == 42
        assert roundtrip_repo.url == "a/url"
        assert roundtrip_repo.bucket_name == "tinpail"
        assert roundtrip_repo.remote_om == None
        assert roundtrip_repo.remote_volume_name == None

        # Second, try remote volume
        repository.credentials = None
        repository.bucket_name = None
        repository.remote_om = "https://me:password@hostname:1234"
        repository.remote_volume_name = "volumeName"

        j_repo = RepositoryConverter.to_json(repository)
        print j_repo

        roundtrip_repo = RepositoryConverter.build_repository_from_json(j_repo)
        assert roundtrip_repo.uuid == "aaaabbbb"
        assert roundtrip_repo.volume_id == 42
        assert roundtrip_repo.url == "a/url"
        assert roundtrip_repo.bucket_name == None
        assert roundtrip_repo.remote_om == "https://me:password@hostname:1234"
        assert roundtrip_repo.remote_volume_name == "volumeName"

    def test_subscription_conversion(self):

        subscription = Subscription()
        subscription.digest = "abcdef01"
        subscription.name = "vogue"
        subscription.volume_id = 11
        subscription.creation_time = 149000267
        subscription.remote_volume = "popular_mechanics"
        subscription.named_credential = NamedCredential(digest="fffff02", name="goodcredential")

        j_sub = SubscriptionConverter.to_json(subscription)
        print j_sub

        deserialized = SubscriptionConverter.build_from_json(j_sub)
        assert deserialized.digest == "abcdef01"
        assert deserialized.name == "vogue"
        assert deserialized.volume_id == 11
        assert deserialized.creation_time == 149000267
        assert deserialized.remote_volume == "popular_mechanics"
        assert deserialized.named_credential.digest == "fffff02"
 
    def test_remote_volume_conversion(self):

        remote_volume = RemoteVolume()

        remote_volume.remote_om_url = "https://me:password@hostname:1234"
        remote_volume.source_volume_name = "sourceVol"
        volume = Volume()
        volume.id = 34  
        volume.name = "TestVolume"
        volume.media_policy = "SSD"
        remote_volume.volume = volume

        j_remote_volume = RemoteVolumeConverter.to_json(remote_volume)
        print j_remote_volume

        roundtrip_remote_volume = RemoteVolumeConverter.build_remote_volume_from_json(j_remote_volume)
        assert roundtrip_remote_volume.remote_om_url == "https://me:password@hostname:1234"
        assert roundtrip_remote_volume.source_volume_name == "sourceVol"
        assert roundtrip_remote_volume.volume.id == 34

    def test_exported_volume_conversion(self):

        exported_volume = ExportedVolume("7/42/2016-08-03T01:41:14",
            "source_vol",
            "ISCSI",
            4800235841,
            16)

        j_exported_volume = ExportedVolumeConverter.to_json(exported_volume)
        print j_exported_volume

        roundtrip = ExportedVolumeConverter.build_exported_volume_from_json(j_exported_volume)
        assert roundtrip.obj_prefix_key == "7/42/2016-08-03T01:41:14"
        assert roundtrip.source_volume_name == "source_vol"
        assert roundtrip.source_volume_type == "ISCSI"
        assert roundtrip.creation_time == 4800235841
        assert roundtrip.blob_count == 16

    def test_safeguard_preset_conversion(self):
        '''Round-trip conversion for ``model.volume.SafeGuardPreset`` object
        '''
        safeguard_preset = SafeGuardPreset(an_id=3, name="safeguard_preset_test")
        safeguard_preset.recurrence_rule.byday = "MO"
        safeguard_preset.recurrence_rule.frequency = "WEEKLY"
        safeguard_preset.recurrence_rule.byhour = 14
        safeguard_preset.recurrence_rule.byminute = 45

        j_str = PresetConverter.safeguard_to_json_string(safeguard_preset)
        print j_str

        # Produces ``model.volume.SafeGuardPreset`` object
        deserialized = PresetConverter.build_safeguard_preset_from_json(j_str)
        assert deserialized.name == "safeguard_preset_test"
        assert deserialized.id == 3
        assert deserialized.recurrence_rule.byday == "MO"
        assert deserialized.recurrence_rule.frequency == "WEEKLY"
        assert deserialized.recurrence_rule.byhour == 14
        assert deserialized.recurrence_rule.byminute == 45
        assert deserialized.recurrence_rule.bymonthday == None
        assert deserialized.recurrence_rule.bymonth == None
        assert deserialized.recurrence_rule.byyearday == None

        # The value 'MINUTELY' was added as an allowed frequency in 1.3.2.
        safeguard_preset2 = SafeGuardPreset(an_id=0, name="safeguard_preset_test2")
        safeguard_preset2.recurrence_rule.frequency = "MINUTELY"
        # Test as list
        safeguard_preset2.recurrence_rule.byhour = [0]
        safeguard_preset2.recurrence_rule.byminute = [5]

        j_str2 = PresetConverter.safeguard_to_json_string(safeguard_preset2)
        print j_str2

        # Produces ``model.volume.SafeGuardPreset`` object
        deserialized2 = PresetConverter.build_safeguard_preset_from_json(j_str2)
        assert deserialized2.name == "safeguard_preset_test2"
        assert deserialized2.id == 0
        assert deserialized2.recurrence_rule.frequency == "MINUTELY"
        assert deserialized2.recurrence_rule.byday == None
        assert deserialized2.recurrence_rule.byhour == [0]
        assert deserialized2.recurrence_rule.byminute == [5]
        assert deserialized2.recurrence_rule.bymonthday == None
        assert deserialized2.recurrence_rule.bymonth == None
        assert deserialized2.recurrence_rule.byyearday == None

