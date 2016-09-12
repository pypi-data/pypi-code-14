from troposphere import Parameter, Ref, Template, Tags, If, Equals, Not, Join
from troposphere.constants import KEY_PAIR_NAME, SUBNET_ID, M4_LARGE, NUMBER
import troposphere.emr as emr
import troposphere.iam as iam


template = Template()
template.add_description(
    "Sample CloudFormation template for creating an EMR cluster"
)

keyname = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "to the instances",
    Type=KEY_PAIR_NAME
))

subnet = template.add_parameter(Parameter(
    "Subnet",
    Description="Subnet ID for creating the EMR cluster",
    Type=SUBNET_ID
))

spot = template.add_parameter(Parameter(
    "SpotPrice",
    Description="Spot price (or use 0 for 'on demand' instance)",
    Type=NUMBER,
    Default="0.1"
))

withSpotPrice = "WithSpotPrice"
template.add_condition(withSpotPrice, Not(Equals(Ref(spot), "0")))

gcTimeRatio = template.add_parameter(Parameter(
    "GcTimeRatioValue",
    Description="Hadoop name node garbage collector time ratio",
    Type=NUMBER,
    Default="19"
))

# IAM roles required by EMR

emr_service_role = template.add_resource(iam.Role(
    'EMRServiceRole',
    AssumeRolePolicyDocument={
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "elasticmapreduce.amazonaws.com"
                ]
            },
            "Action": ["sts:AssumeRole"]
        }]
    },
    ManagedPolicyArns=[
        'arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole'
    ]
))

emr_job_flow_role = template.add_resource(iam.Role(
    "EMRJobFlowRole",
    AssumeRolePolicyDocument={
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "ec2.amazonaws.com"
                ]
            },
            "Action": ["sts:AssumeRole"]
        }]
    },
    ManagedPolicyArns=[
        'arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role'
    ]
))

emr_instance_profile = template.add_resource(iam.InstanceProfile(
    "EMRInstanceProfile",
    Roles=[Ref(emr_job_flow_role)]
))

# EMR Cluster Resource

cluster = template.add_resource(emr.Cluster(
    "EMRSampleCluster",
    Name="EMR Sample Cluster",
    ReleaseLabel='emr-4.4.0',
    BootstrapActions=[emr.BootstrapActionConfig(
        Name='Dummy bootstrap action',
        ScriptBootstrapAction=emr.ScriptBootstrapActionConfig(
            Path='file:/usr/share/aws/emr/scripts/install-hue',
            Args=["dummy", "parameter"]
        )
    )],
    Configurations=[
        emr.Configuration(
            Classification="core-site",
            ConfigurationProperties={
                'hadoop.security.groups.cache.secs': '250'
            }
        ),
        emr.Configuration(
            Classification="mapred-site",
            ConfigurationProperties={
                'mapred.tasktracker.map.tasks.maximum': '2',
                'mapreduce.map.sort.spill.percent': '90',
                'mapreduce.tasktracker.reduce.tasks.maximum': '5'
            }
        ),
        emr.Configuration(
            Classification="hadoop-env",
            Configurations=[
                emr.Configuration(
                    Classification="export",
                    ConfigurationProperties={
                        "HADOOP_DATANODE_HEAPSIZE": "2048",
                        "HADOOP_NAMENODE_OPTS": Join("", ["-XX:GCTimeRatio=",
                                                          Ref(gcTimeRatio)])
                    }
                )
            ]
        )
    ],
    JobFlowRole=Ref(emr_instance_profile),
    ServiceRole=Ref(emr_service_role),
    Instances=emr.JobFlowInstancesConfig(
        Ec2KeyName=Ref(keyname),
        Ec2SubnetId=Ref(subnet),
        MasterInstanceGroup=emr.InstanceGroupConfigProperty(
            Name="Master Instance",
            InstanceCount="1",
            InstanceType=M4_LARGE,
            Market="ON_DEMAND"
        ),
        CoreInstanceGroup=emr.InstanceGroupConfigProperty(
            Name="Core Instance",
            BidPrice=If(withSpotPrice, Ref(spot), Ref("AWS::NoValue")),
            Market=If(withSpotPrice, "SPOT", "ON_DEMAND"),
            EbsConfiguration=emr.EbsConfiguration(
                EbsBlockDeviceConfigs=[
                    emr.EbsBlockDeviceConfigs(
                        VolumeSpecification=emr.VolumeSpecification(
                            SizeInGB="10",
                            VolumeType="gp2"
                        ),
                        VolumesPerInstance="1"
                    )
                ],
                EbsOptimized="true"
            ),
            InstanceCount="1",
            InstanceType=M4_LARGE,
        )
    ),
    Applications=[
        emr.Application(Name="Hadoop"),
        emr.Application(Name="Hive"),
        emr.Application(Name="Mahout"),
        emr.Application(Name="Pig"),
        emr.Application(Name="Spark")
    ],
    VisibleToAllUsers="true",
    Tags=Tags(
        Name="EMR Sample Cluster"
    )
))

step = template.add_resource(emr.Step(
    'TestStep',
    Name="TestStep",
    ActionOnFailure='CONTINUE',
    HadoopJarStep=emr.HadoopJarStepConfig(
        Args=["5", "10"],
        Jar="s3://emr-cfn-test/hadoop-mapreduce-examples-2.6.0.jar",
        MainClass="pi",
        StepProperties=[
            emr.KeyValue('my.custom.property', 'my.custom.value')
        ]
    ),
    JobFlowId=Ref(cluster)
))

print(template.to_json())
