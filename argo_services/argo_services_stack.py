from aws_cdk import core
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2


# serices = [nginx]

# task_def_services = []


class ArgoServicesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        fargate_task_definition = ecs.FargateTaskDefinition(self, "tryservice",
            memory_limit_mib=512,
            cpu=256
        )

        container = fargate_task_definition.add_container("WebContainer",
            # Use an image from ECR
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            # secrets={# Retrieved from AWS Secrets Manager or AWS Systems Manager Parameter Store at container start-up.
            #     "SECRET": ecs.Secret.from_secrets_manager(secret),
            #     "DB_PASSWORD": ecs.Secret.from_secrets_manager(db_secret, "password"), # Reference a specific JSON field
            #     "PARAMETER": ecs.Secret.from_ssm_parameter(parameter)}
        )

        container.add_port_mappings(
            ecs.PortMapping(container_port=80)
        )

        vpc = ec2.Vpc.from_lookup(self,"ecs-vpc", vpc_id="vpc-05390e1e390cd8f81")

        cluster = ecs.Cluster.from_cluster_attributes(self,"cluster",cluster_name="try", vpc=vpc, security_groups=[], cluster_arn=" arn:aws:ecs:us-east-1:541986371853:cluster/try")

        service = ecs.FargateService(self, "Service", cluster=cluster, task_definition=fargate_task_definition, desired_count=1)

        # lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        # lb = elbv2.ApplicationLoadBalancer.fromApplicationLoadBalancerAttribute(self,"LB",loadBalancerArn="")
        # listener = lb.add_listener("Listener", port=80)
        listener = elbv2.ApplicationListener.from_application_listener_attributes(self, "ArgoListner", listener_arn="arn:aws:elasticloadbalancing:us-east-1:541986371853:listener/app/trylb/d904ee464af786fe/ac846bb6f0d76e5c"
        ,default_port=80, security_group_id="sg-018c3eb117f9a1fea")


        tg = elbv2.ApplicationTargetGroup(self, "tg", vpc=vpc, port=80, targets=[service], health_check=elbv2.HealthCheck(path="/", port="80"))

        listener.add_target_groups("tgid", target_groups=[tg], priority=1, path_pattern="/index")

        # target_group1 = listener.add_targets("try-tg",
        #     port=80,
        #     targets=[service],
        #     target_group_name="try-tg",
        #     path_pattern="/try-path",
        #     priority=1
        # )