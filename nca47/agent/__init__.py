from oslo_config import cfg
from oslo_log import log as logging
from nca47.agent import cli_driver
from nca47.agent import dns_driver
from nca47.agent import firewall_driver
from nca47.common import exception
from nca47.common.i18n import _

LOG = logging.getLogger(__name__)

DRIVER_OPTS = [
    cfg.StrOpt('dns_driver', default='zdns',
               help=_('The dns driver for nca47 calling.')),
    cfg.StrOpt('firewall_driver', default='fake',
               help=_('The firewall driver for nca47 calling.')),
    cfg.StrOpt('cli_driver', default='cli',
               help=_('The backend device type for nca47 in calling.'))
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='backend_driver',
                         title='Options for the backend device service')
CONF.register_group(opt_group)

CONF.register_opts(DRIVER_OPTS, opt_group)


def get_dns_backend():
    LOG.debug("Loading dns backend driver by conf file")
    driver_name = CONF.backend_driver.dns_driver
    if driver_name == 'zdns':
        return dns_driver.zdns_driver.dns_zone_driver.get_instance()
    elif driver_name == 'fake':
        return dns_driver.fake_driver.fake_dns_driver.get_instance()
    else:
        raise exception.DriverNotFound(driver_name=driver_name)


def get_firewall_backend():
    LOG.debug("Loading firewall backend driver by conf file")
    driver_name = CONF.backend_driver.firewall_driver
    if driver_name == 'fw':
        return firewall_driver.fw_driver.fw_driver.get_instance()
#         return fw_driver.zdns_driver.dns_zone_driver.get_instance()
    elif driver_name == 'fake':
        return firewall_driver.fake_driver.fake_driver.get_instance()
    else:
        raise exception.DriverNotFound(driver_name=driver_name)


def get_cli_backend(**kwargs):
    """
    Get backend command-line interface device
    """
    LOG.debug("Loading backend command-line interface infos by conf file")
    driver_name = CONF.backend_driver.cli_driver
    if driver_name == 'cli':
        return cli_driver.clios
    else:
        raise exception.DriverNotFound(driver_name=driver_name)
