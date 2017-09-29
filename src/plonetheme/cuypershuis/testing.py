# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import plonetheme.cuypershuis


class PlonethemeModernBaseLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plonetheme.cuypershuis)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetheme.cuypershuis:default')


PLONETHEME_MODERNBASE_FIXTURE = PlonethemecuypershuisLayer()


PLONETHEME_MODERNBASE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONETHEME_MODERNBASE_FIXTURE,),
    name='PlonethemecuypershuisLayer:IntegrationTesting'
)


PLONETHEME_MODERNBASE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONETHEME_MODERNBASE_FIXTURE,),
    name='PlonethemecuypershuisLayer:FunctionalTesting'
)


PLONETHEME_MODERNBASE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONETHEME_MODERNBASE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PlonethemecuypershuisLayer:AcceptanceTesting'
)
