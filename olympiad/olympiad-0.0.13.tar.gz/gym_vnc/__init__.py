import logging
import os

from gym.envs.registration import register

import gym_vnc.configuration
from gym_vnc import error, envs
from gym_vnc.remotes import docker_remote
from gym_vnc.rewarder import merge_infos
from gym_vnc.runtimes.registration import runtime_spec

logger = logging.getLogger(__name__)

def enable_logfile(path=None):
    if path is None:
        path = '/tmp/gym-vnc-{}.log'.format(os.getpid())

    root_logger = logging.getLogger()
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler = logging.FileHandler(path, 'w')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

def docker_image(runtime_id):
    logger.warn('DEPRECATION WARNING: gym_vnc.docker_image(runtime_id) is deprecated and will be removed soon. Use runtime_spec(runtime_id).image instead. ')
    return runtime_spec(runtime_id).image


# Should be exactly the same as CartPole-v0
register(
    id='VNCCartPoleLowDSync-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    tags={
        'vnc': True,
        'core': True,
        'runtime': 'vnc-core-envs',
    },
    kwargs={
        'vnc_pixels': False,
        'core_env_id': 'CartPole-v0',
},
    # experience_limit=1000,
    trials=2,
    timestep_limit=500,
)

# Dynamics should match CartPole-v0, but have pixel observations
register(
    id='VNCCartPoleSync-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    tags={
        'vnc': True,
        'core': True,
        'runtime': 'vnc-core-envs',
    },
    kwargs={
        'core_env_id': 'CartPole-v0',
    },
    # experience_limit=1000,
    trials=2,
    timestep_limit=500,
)

# Async cartpole with 4-d observations
register(
    id='VNCCartPoleLowD-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
    tags={
        'vnc': True,
        'core': True,
        'runtime': 'vnc-core-envs',
    },
    kwargs={
        'vnc_pixels': False,
        'core_env_id': 'CartPole-v0',
    },
    # experience_limit=1000,
    trials=2,
    timestep_limit=500,
)

register(
    id='VNCCartPole-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
    tags={
        'vnc': True,
        'core': True,
        'runtime': 'vnc-core-envs',
    },
    kwargs={
        'core_env_id': 'CartPole-v0',
    },
    # experience_limit=1000,
    trials=2,
    timestep_limit=500,
)

register(
    id='PongShortSync-v3',
    entry_point='gym_vnc.envs.short_env:ShortEnv',
    kwargs={
        'timestep_limit': 10,
        'env_entry_point': 'gym.envs.atari:AtariEnv',
        'env_kwargs': {
            'game': 'pong', 'obs_type': 'image'
        }
    },
    timestep_limit=10,
)

register(
    id='VNCPongShortSync-v3',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    tags={
        'vnc': True,
        'core': True,
        'runtime': 'vnc-core-envs',
    },
    kwargs={
        'core_env_id': 'PongShortSync-v3',
    },
    timestep_limit=10,
)

register(
    id='PitfallShortSync-v3',
    entry_point='gym_vnc.envs.short_env:ShortEnv',
    kwargs={
        'timestep_limit': 10,
        'env_entry_point': 'gym.envs.atari:AtariEnv',
        'env_kwargs': {
            'game': 'pitfall', 'obs_type': 'image'
        }
    },
    timestep_limit=10,
)

register(
    id='VNCPitfallShortSync-v3',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    tags={
        'vnc': True,
        'core': True,
        'runtime': 'vnc-core-envs',
    },
    kwargs={
        'core_env_id': 'PitfallShortSync-v3',
    },
    # experience_limit=1000,
    timestep_limit=10,
)

# VNCAtari
for game in ['air_raid', 'alien', 'amidar', 'assault', 'asterix',
             'asteroids', 'atlantis', 'bank_heist', 'battle_zone',
             'beam_rider', 'berzerk', 'bowling', 'boxing', 'breakout',
             'carnival', 'centipede', 'chopper_command', 'crazy_climber',
             'demon_attack', 'double_dunk', 'elevator_action', 'enduro',
             'fishing_derby', 'freeway', 'frostbite', 'gopher', 'gravitar',
             'ice_hockey', 'jamesbond', 'journey_escape', 'kangaroo', 'krull',
             'kung_fu_master', 'montezuma_revenge', 'ms_pacman',
             'name_this_game', 'phoenix', 'pitfall', 'pong', 'pooyan',
             'private_eye', 'qbert', 'riverraid', 'road_runner', 'robotank',
             'seaquest', 'skiing', 'solaris', 'space_invaders', 'star_gunner',
             'tennis', 'time_pilot', 'tutankham', 'up_n_down', 'venture',
             'video_pinball', 'wizard_of_wor', 'yars_revenge', 'zaxxon']:
    # space_invaders should yield SpaceInvaders-v0 and SpaceInvaders-ram-v0
    base = ''.join([g.capitalize() for g in game.split('_')]) # SpaceInvaders

    for version in [0, 3]:
        core_env_id = '{}-v{}'.format(base, version) # e.g. SpaceInvaders-v3
        register(
            id='VNC{}'.format(core_env_id),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': core_env_id,
            },
            # experience_limit=1000,
            timestep_limit=100000,
        )

        register(
            id='VNC{}Sync-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': core_env_id,
            },
            # experience_limit=1000,
            timestep_limit=100000,
        )

        register(
            id='VNC{}30FPS-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': core_env_id,
                'fps': 30,
            },
            # experience_limit=1000,
            timestep_limit=100000,
        )

        register(
            id='VNC{}Slow-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': core_env_id,
                'fps': 15,
            },
            # experience_limit=1000,
            timestep_limit=100000,
        )

        deterministic_core_env_id = '{}Deterministic-v{}'.format(base, version) # e.g. SpaceInvadersDeterministic-v3

        register(
            id='VNC{}Deterministic-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': deterministic_core_env_id,
            },
            timestep_limit=100000,
        )
        register(
            id='VNC{}DeterministicSlow-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': deterministic_core_env_id,
                'fps': 15,
            },
            timestep_limit=75000,
        )
        register(
            id='VNC{}DeterministicSync-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': deterministic_core_env_id,
            },
            # experience_limit=1000,
            timestep_limit=75000,
        )

        no_frameskip_core_env_id = '{}NoFrameskip-v{}'.format(base, version) # e.g. SpaceInvadersNoFrameskip-v3
        register(
            id='VNC{}NoFrameskip-v{}'.format(base, version),
            entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
            tags={
                'vnc': True,
                'core': True,
                'atari': True,
                'runtime': 'vnc-core-envs',
            },
            kwargs={
                'core_env_id': no_frameskip_core_env_id,
            },
            # experience_limit=1000,
            timestep_limit=400000
        )

metadata_v1 = {
    'type': 'qrcode',
    'x': 914,
    'y': 658,
    'width': 100,
    'height': 100,
}

# VNCFlashgames

for game in [
    # Please keep this mirrored with the benchmarks in
    # https://github.com/openai/gym-vnc-envs/blob/master/vnc-flashgames/gym_flashgames/__init__.py

    # VNCFlashRacing-v0
        'VNCCarTitansMinicarHunt-v0',
        'VNCCarTitansSpaceColony-v0',
        'VNCCarTitansSpeedBusters-v0',
        'VNCKongregateAmericanRacing-v0',
        'VNCKongregateCoasterRacer-v0',
        'VNCKongregateCoasterRacer2-v0',
        'VNCKongregateCoasterRacer2Bike-v0',
        'VNCKongregateCoastRunners-v0',
        'VNCKongregateDriftRunners-v0',
        'VNCKongregateDriftRunners2-v0',
        'VNCKongregateDuskDrive-v0',
        'VNCKongregateFormulaRacer-v0',
        'VNCKongregateFormulaRacer2012-v0',
        'VNCKongregateGrandPrixGo-v0',
        'VNCKongregateHeatRushFuture-v0',
        'VNCKongregateHeatRushUsa-v0',
        'VNCKongregateNeonRace-v0',
        'VNCKongregateNeonRace2-v0',
        'VNCKongregateRollerRider-v0',
        'VNCKongregateSpacePunkRacer-v0',
        'VNCNotDopplerThundercars-v0',
        'VNCTurboNukeClubNitro-v0',
        'VNCY8EvolutionRacing-v0',
        'VNCKongregateGunExpress-v0',
        'VNCNotDopplerTurboRally-v0', #ocr not 100% - move bg and includes #s
        'VNCFreegamesforyourwebsiteMotoMadness-v0', #rare distractor #s could mess
        'VNCCarTitansEvasiveRacers-v0',
        'VNCWillingGames3dBuggyRacing-v0', # error'd on a screen tear filter caught
        'VNCWillingGamesCircuitSuperCarsRacing-v0', #think passed playthrough
        'VNCNotDopplerOffroaders-v0', #position
        'VNCInsaneheroV8MuscleCars-v0', #position
        'VNCKongregateCruisin-v0', # position

        # Has vexpect, current scorer doesn't work
        'VNCCarTitans3DLaSupercars2-v0', #stripes
        'VNCCarTitansDodgeAndCrash-v0', #digital/segment display

        # Has vexpect, needs scorer

        'VNCFreeGamesForYourWebsiteUrbanMicroRacers-v0',
        'VNCCarTitans3DUrbanMadness2-v0',
        'VNCFreeGamesForYourWebsiteWheelers-v0',
        'VNCNotDopplerGrandPrixGo2-v0',
        'VNCNotDopplerOffroaders2-v0',
        'VNCCarTitansDuskRacers-v0', # money
        'VNCArmorGamesKartOn-v0', # speed
        'VNCWillingGamesF1RacingChallenge-v0', # numerical
        'VNCCarTitans3dSportRampage-v0', # distance bar
        'VNCCarTitans3dSuperRide-v0', # distance bar
        'VNCCarTitans3dRookieCop-v0', # distance bar or speedometer
        'VNCCarTitans3dFlashRacer-v0', # distance bar or speedometer
        'VNCCarTitansRedFuryRacing-v0', # speedometer
        'VNCCarTitansDumperRush-v0',
        'VNCCarTitansAdrenalineChaser-v0', # speedometer
        'VNCCarTitansAngryNewsVan-v0', # speedometer or targets
        'VNCCarTitansMotorWheels-v0', # speedometer or targets
        'VNCCarTitansTurboCrew-v0',
        'VNCCarTitansVirtualRacer-v0', # speedometer or targets
        'VNCJohnnyTwoShoesHighSpeedChase-v0', # score/speed
        'VNCCarTitansVengeanceRider-v0',
        'VNCCarTitansArmySpeeder-v0',
        'VNCCarTitansArmyPursuit-v0', # speedometer/targets
        'VNCCarTitansHighwayRevenge-v0', # speedometer/targets
        'VNCY8TaxiRacers-v0', # speed
        'VNCCarTitansShift-v0', # hard to read speed
        'VNCCarTitans3dFuriousDriver-v0', # remaining time

        # Has vexpect, sparse rewards

        'VNCNotDopplerSuperbikeRacer-v0', # need to parse position
        'VNCFreegamesforyourwebsiteSuperbikeExtreme-v0', # position if needed
        'VNCFreegamesforyourwebsitePickUpTruckRacing-v0', # position
        'VNCNotDopplerHighwayOfTheDead-v0', # points flash on screen
        'VNCWillingGamesMiniMachines-v0', # position + lap
        'VNCWillingGamesV8RacingChampion-v0', # lap
        'VNCWillingGamesNewSiberianSupercarsRacing-v0', # lap
        'VNCInsaneheroV8MuscleCars2-v0', # position
        'VNCInsaneheroV8MuscleCars3-v0', # position
        'VNCInsaneheroStreetrace2Nitro-v0', # position
        'VNCInsaneheroStreetRace3-v0', # position
        'VNCTurbonukePoliceChaseCrackdown-v0', # arrest count
        'VNCFreegamesforyourwebsiteSchoolBusRacing-v0', # position
        'VNCFreegamesforyourwebsiteDrifters-v0', # position, also a numeric gear count (1-4)
        'VNCWillingGamesRacingSupercarChampionship-v0', # lap
        'VNCInsaneheroMonsterTruckRally-v0', # position
        'VNCFreegamesforyourwebsiteTinyRacers-v0', # position
        'VNCFreegamesforyourwebsiteGoKart3d-v0', # position
        'VNCFreegamesforyourwebsiteOffRoaders2-v0', # position/lap
        'VNCFreegamesforyourwebsiteLawnmowerRacing3d-v0', # position/lap
        'VNCFreegamesforyourwebsiteCanyonValleyRally-v0', # position
        'VNCFreegamesforyourwebsiteOffRoaders3d-v0', # position
        'VNCWillingGamesPoliceHotRacing-v0', # position
        'VNCTurbonukeWreckRoad-v0', # position
        'VNCCarTitansToyRacers-v0', # targets destroyed
        'VNCCarTitansEpicDerbyRace-v0', # targets destroyed
        'VNCCarTitansSupercarDomination-v0', # targets destroyed
        'VNCArmorGamesFlashRacer-v0', # position/lap

        # Has vexpect, no obvious reward
        'VNCInsaneheroSuperRallyChallenge-v0', # could do time / checkpoint numbers
        'VNCInsaneheroSuperRallyChallenge2-v0', # could do time / checkpoint numbers
        'VNCCarTitans3dUrbanMadness-v0',
        'VNCCarTitans3dTruckInTheWoods-v0',
        'VNCCarTitans3dTestDrive-v0',
        'VNCCarTitansRoadblockAttack-v0', # could do amount of time alive or seconds from exploding
        'VNCCarTitansTheRoadIsMine-v0',
        'VNCCarTitans3dClassicRacing-v0',
        'VNCCarTitans3dSpeedFever-v0',
        'VNCCarTitans3dRallyFever-v0',
        'VNCCarTitansDeepForest3dRace-v0',

        # Registered but not yet integrated

        # 'VNCNotDopplerDriftRunners3d-v0', # requires clicks through modals to play
        # 'VNCFreegamesforyourwebsitePoliceInterceptor-v0', # requires clicks through modals to play

    # VNCDebug-v0
        'VNCKongregateDuskDriveDebug-v0',

    # VNCFlashMatching-v0
        'VNCArkadiumEggzBlast-v0',
        'VNCArkadiumMonkeyGems-v0',
        'VNCArkadiumSparks-v0',
        'VNCArkadiumTrizzle-v0',
        'VNCArkadiumTumbleTiles-v0',
        'VNCFreegamesforyourwebsiteFlashBombs-v0',
        'VNCFreegamesforyourwebsiteHarvestDay-v0',
        'VNCFreegamesforyourwebsiteCosmicSwitch-v0',
        'VNCFreegamesforyourwebsiteConnect2-v0',
        'VNCFreegamesforyourwebsiteMatchTheBugz-v0',
        'VNCFreegamesforyourwebsiteJungleCrash-v0',
        'VNCFreegamesforyourwebsiteLuckyBalls-v0',
        'VNCSpilGamesEasterBubbles-v0',
        'VNCSpilGamesCupidBubbles-v0',
        'VNCSpilGamesChristmasBubbles-v0',
        'VNCSpilGamesDragonChain-v0',
        'VNCSpilGamesIceBlock-v0',
        'VNCSpilGamesBubbleGlee-v0',
        'VNCSpilGamesPrincessBubblesRescuePrince-v0',
        'VNCSpilGamesYummyyummyMonsterShooter-v0',
        'VNCSpilGamesBubbleMover-v0',
        'VNCSpilGamesBubbleHitValentine-v0',
        'VNCSpilGamesBubbleHitChristmas-v0',
        'VNCSpilGamesPinBalls-v0',
        'VNCSpilGamesBubbleHitPonyParade-v0',
        'VNCSpilGamesBubbleHitHalloween-v0',
        'VNCSpilGamesBubbleHit-v0',

        'VNCArmorgamesPuzzleRescuePrime-v0',
        'VNCKongregateGalacticGems-v0',
        'VNCKongregateGalacticGems2-v0',
        'VNCKongregateGalacticGems2Accelerated-v0',
        'VNCKongregateGalacticGems2LevelPack-v0',
        'VNCKongregateGalacticGems2NewFrontiers-v0',
        'VNCKongregateSmileyPuzzle2-v0',
        'VNCKongregateWinterSlider-v0',
        'VNCMatch3Gemclix-v0',
        'VNCNeongamesBottleCaps-v0',
        'VNCNeongamesCandyMatch-v0',
        'VNCNeongamesHappyEasterEggs-v0',
        'VNCNeongamesMatchAroundTheWorld-v0',
        'VNCNeongamesOceanMatch-v0',
        'VNCNeongamesRapaNui-v0',
        'VNCNeongamesSnowQueen-v0',
        'VNCSmileygamerCandySlider-v0',
        'VNCSmileygamerEasterEggSlider-v0',
        'VNCSmileygamerSmileyJumpFest-v0',
        'VNCSmileygamerSmileyPuzzle-v0',
        'VNCSmileygamerSmileyPuzzleGirlEdition-v0',
        'VNCSmileygamerZombieMatch3-v0',
        'VNCSpilgames1001ArabianNights-v0',
        'VNCSpilgamesAladdinAndTheWonderLamp-v0',
        'VNCSpilgamesBubbleTub-v0',
        'VNCSpilgamesDreamChristmasLink-v0',
        'VNCSpilgamesEasterBunnyEggs-v0',
        'VNCSpilgamesEctoHarvest-v0',
        'VNCSpilgamesFunnyEaster-v0',
        'VNCSpilgamesGalaxyMission-v0',
        'VNCSpilgamesHappyBees-v0',
        'VNCSpilgamesHeySummer-v0',
        'VNCSpilgamesMoosters-v0',
        'VNCSpilgamesMysteriousPirateJewels-v0',
        'VNCSpilgamesMysticIndiaPop-v0',
        'VNCSpilgamesPenguinCubes-v0',
        'VNCSpilgamesSnowQueen3-v0',
        'VNCSpilgamesSnowQueen4-v0',
        'VNCSpilgamesStickylinky-v0',
        'VNCSpilgamesSwapTheDots-v0',
        'VNCSpilgamesTastyFruits-v0',
        'VNCSpilgamesUnderwaterSecrets-v0',
        'VNCSpilgamesZodiacMatch-v0',
        'VNCY8BubbleShooterChallenge-v0',
        'VNCY8EasterEggsChallenge-v0',
        'VNCY8GemPop-v0',
        'VNCY8JellyFriend-v0',
        'VNCY8JollySwipe-v0',
        'VNCY8JollySwipeLevelPack-v0',
        'VNCY8MarblesShooter-v0',


    # VNCPlatform-v0
        # Fully integrated
        'VNCAndkonWeirdville-v0',
        'VNCMiniclipRedBeard-v0',
        'VNCMiniclipMimelet-v0',
        'VNCArmorGamesJamesTheCircusZebra-v0',
        'VNCArmorGamesJamesTheSpaceZebra-v0',

        # Vexpect, no scorer
        'VNCMiniclipDaleAndPeakot-v0',
        'VNCMiniclipZombality-v0',
        'VNCMiniclipAcidFactory-v0',
        'VNCMiniclipPanikInChocoland-v0',
        'VNCMiniclipZed-v0',
        'VNCFreegamesforyourwebsiteParkour-v0',
        'VNCFreegamesforyourwebsiteCakeQuest-v0',
        'VNCFreegamesforyourwebsiteDetectiveConrad-v0',
        'VNCFreegamesforyourwebsiteAlien-v0',
        'VNCFreegamesforyourwebsitePixelQuest-v0',
        'VNCFreegamesforyourwebsiteSpaceBounty-v0',
        'VNCFreegamesforyourwebsiteSuperK9-v0',
        'VNCSpilGamesPrincessToTheRescue-v0',
        'VNCSpilGamesRbots-v0',
        'VNCSpilGamesTitanic-v0',
        'VNCSpilGamesItsDarkInHell-v0',
        'VNCSpilGamesNinjaPainter-v0',
        'VNCSpilGamesMineDrop-v0',
        'VNCSpilGamesAliceNixsAdventure-v0',
        'VNCSpilGamesFatWarrior2-v0',
        'VNCFreegamesforyourwebsiteZombiesAndDonuts-v0',
        'VNCFreegamesforyourwebsitePointless-v0',
        'VNCFreegamesforyourwebsiteKnockers-v0',
        'VNCFreegamesforyourwebsiteTheProfessionals3-v0',
        'VNCFreegamesforyourwebsiteCloseCombat-v0',
        'VNCSpilGamesCrystalCurse-v0',
        'VNCSpilGamesCosmoGravity2-v0',
        'VNCSpilGamesLevelEditor3-v0',
        'VNCSpilGamesReverseBoots-v0',
        'VNCSpilGamesLazerman-v0',
        'VNCSpilGamesQoosh-v0',
        'VNCSpilGamesResonance-v0',
        'VNCSpilGamesThaw-v0',
        'VNCSpilGamesPenguinHeroes-v0',
        'VNCSpilGamesJumpz-v0',
        'VNCSpilGamesTwinkleStarRush-v0',
        'VNCSpilGamesCloud9-v0',
        'VNCMiniclipGravityGuy-v0',
        'VNCMiniclipFredFigglehorn-v0',
        'VNCMiniclipAdventuresOfBloo-v0',
        'VNCMiniclip3FootNinja-v0',
        'VNCMiniclip3FootNinjaIi-v0',
        'VNCFreegamesforyourwebsiteNinjaTrainingWorlds-v0',
        'VNCFreegamesforyourwebsiteRocketeer-v0',
        'VNCFreegamesforyourwebsiteOverheat-v0',
        'VNCFreegamesforyourwebsiteSweetTooth-v0',
        'VNCFreegamesforyourwebsiteBloodbathBay-v0',
        'VNCFreegamesforyourwebsiteHamsterball-v0',
        'VNCFreegamesforyourwebsiteGolfRun-v0',
        'VNCFreegamesforyourwebsiteSwampTreck-v0',
        'VNCFreegamesforyourwebsiteDancingWithShadows-v0',
        'VNCSpilGamesIcs2-v0',
        'VNCSpilGamesZombonarium-v0',
        'VNCSpilGamesAmigoPancho4Travel-v0',
        'VNCSpilGamesBlobsStory-v0',
        'VNCSpilGamesSupergirlGo-v0',
        'VNCSpilGamesElainesBakery-v0',
        'VNCSpilGamesBombIt6-v0',
        'VNCSpilGamesSnailBob4-v0',
        'VNCSpilGamesAmigoPancho3SheriffSancho-v0',
        'VNCSpilGamesSpacemanMax-v0',
        'VNCSpilGamesBombIt4-v0',
        'VNCSpilGamesNuttyBoom-v0',
        'VNCSpilGamesCarsVsRobots-v0',
        'VNCSpilGamesThePretenderPartThree-v0',
        'VNCSpilGamesTechnoMania-v0',
        'VNCSpilGamesBobbyNutcaseMotoJumping-v0',
        'VNCSpilGamesDiscoverEurope-v0',
        'VNCSpilGamesBimmin2-v0',
        'VNCSpilGamesFlowerSolitaire-v0',
        'VNCSpilGamesTamusMitta-v0',
        'VNCSpilGamesRollingHills-v0',
        'VNCSpilGamesFeedOurDoughnutOverlords-v0',
        'VNCSpilGamesSafariTime-v0',
        'VNCSpilGamesAmigoPancho-v0',
        'VNCSpilGamesSlipSlideSloth-v0',
        'VNCSpilGamesUrbanFatburner-v0',
        'VNCSpilGamesDragonChronicles-v0',
        'VNCSpilGamesMidnightCanine-v0',
        'VNCSpilGamesBlackForce-v0',
        'VNCSpilGamesHeavenAndHell-v0',
        'VNCSpilGamesZombiesMustDie-v0',
        'VNCSpilGamesCrane-v0',
        'VNCSpilGamesCastleSolitaire-v0',
        'VNCFreegamesforyourwebsiteEvilMinion-v0',
        'VNCMiniclipCommando2-v0',
        'VNCMiniclipTumblestump2-v0',
        'VNCMiniclipRunNGun-v0',
        'VNCMiniclipRedCode3-v0',
        'VNCMiniclipObamaAlienDefense-v0',
        'VNCMiniclipRoboPop-v0',
        'VNCMiniclipBushRoyalRampage-v0',
        'VNCMiniclipDeepFreeze-v0',
        'VNCMiniclipCommando-v0',
        'VNCMiniclipCableCapers2-v0',
        'VNCFreegamesforyourwebsitePickAndDig2-v0',
        'VNCFreegamesforyourwebsiteFartBlaster-v0',
        'VNCFreegamesforyourwebsiteGoGreenGo-v0',
        'VNCSpilGamesZevil2-v0',
        'VNCSpilGamesDeathCabin-v0',
        'VNCSpilGamesVideoGameMonster-v0',
        'VNCSpilGamesSistersOfNoMercy-v0',
        'VNCSpilGamesUnfreezeMe3-v0',
        'VNCSpilGamesExperimentalShooter2-v0',
        'VNCSpilGamesHelmetBombers3-v0',
        'VNCSpilGamesFinalNinjaZero-v0',
        'VNC2pgFreakyRun-v0',
        'VNC2pgGunnerMayhem-v0',
        'VNC2pgGonAndMon-v0',
        'VNC2pgAstroman-v0',
        'VNCPlatformgamesQubedMysteriousIsland-v0',
        'VNC2pgNinjaPandaArena-v0',
        'VNC2pgRunRamRun-v0',
        'VNC2pgBubblePop-v0',
        'VNC2pgMineHero-v0',
        'VNC2pgRetroRunner-v0',
        'VNC2pgSuperGunners-v0',
        'VNC2pgLuxUltimate-v0',
        'VNC2pgRainbowDrops-v0',
        'VNC2pgNadiasRage-v0',
        'VNC2pgWaveLucha-v0',
        'VNC2pgUltimateEscape-v0',
        'VNC2pgSuperDash-v0',
        'VNC2pgBoltThrough-v0',
        'VNC2pgNinjaPandaCouple-v0',
        'VNC2pgKawairun-v0',
        'VNCY8HeroRoofTop-v0',
        'VNCY8BraveAstronaut-v0',
        'VNCY8StrikeForceKitty-v0',

    #VNCFlashTowerDefense-v0
        'VNCFreegamesforyourwebsiteAlienAssault-v0',
        'VNCFreegamesforyourwebsiteCarrotFantasyExtreme2-v0',
        'VNCFreegamesforyourwebsiteTheThreeTowers-v0',
        'VNCFreegamesforyourwebsiteCarrotFantasyExtreme3-v0',
        'VNCFreegamesforyourwebsiteCarrotFantasy2Undersea-v0',
        'VNCFreegamesforyourwebsiteCarrotFantasy2Desert-v0',
        'VNCFreegamesforyourwebsiteTheBoomlandsWorldWars-v0',
        'VNCFreegamesforyourwebsiteCarrotFantasy-v0',
        'VNCFreegamesforyourwebsiteNukeDefense-v0',
        'VNCFreegamesforyourwebsiteTowerMoon-v0',
        'VNCFreegamesforyourwebsiteStalingrad-v0',
        'VNCFreegamesforyourwebsiteMushroomFarmDefender-v0',
        'VNCFreegamesforyourwebsiteStalingrad3-v0',
        'VNCFreegamesforyourwebsiteStalingrad2-v0',
        'VNCSpilGamesFlowerGuardian-v0',
        'VNCSpilGamesFinalSiege-v0',
        'VNCSpilGamesHandsOff-v0',
        'VNCSpilGamesFairyDefense-v0',
        'VNCSpilGamesWorldsGuard2-v0',
        'VNCSpilGamesWilliamTell-v0',
        'VNCSpilGamesZombieTdReborn-v0',
        'VNCSpilGamesZombieTowerDefenseReborn-v0',
        'VNCSpilGamesMeerkatMission-v0',
        'VNCSpilGamesPaperDefense-v0',
        'VNCSpilGamesSnowPrincessMakeup-v0',
        'VNCSpilGamesEpicDefender-v0',
        'VNCY8Devilment-v0',
        'VNCY8BraveHeads-v0',
        'VNCY8IslandDefense-v0',
        'VNCY8KeeperOfTheGrove3-v0',
        'VNCY8WarHeroes-v0',
        'VNCKongregateGiantsAndDwarvesTd-v0',
        'VNCNotDopplerCursedTreasureDontTouchMyGems-v0',
        'VNCArmorGamesGemcraft-v0',
        'VNCArmorGamesBubbleTanksTd15-v0',
        'VNCArmorGamesPicnicPanicTd-v0',

    #VNCFlashAssorted-v0
        'VNCArmorGamesKnighttron-v0',
        'VNCNotDopplerPiggyWiggy-v0',
        'VNCGamesButlerSnakeClassic-v0',
        'VNCGamesButlerLong_short-v0',
        'VNCGamesButlerMonsterRun-v0',
        'VNC2pgEatToWin-v0',
        'VNCNotDopplerBunnyCannon-v0',
        'VNCArmorGamesHearts-v0',
        'VNCArmorGamesMultiballMadness-v0',
        'VNCArmorGamesPel-v0',
        'VNC1000WebGamesBasement-v0',
        'VNC2pgFoosball2Player-v0',
        'VNCArmorGamesColordefense-v0',
        'VNCArmorGamesRunSoldierRun-v0',
        'VNCArmorGamesTrickOrToad-v0',
        'VNCArmorGamesSpinSprint-v0',
        'VNCArmorGamesSpinSoar-v0',
        'VNCArmorGamesRose-v0',
        'VNCArmorGamesMusicSmash-v0',
        'VNCArmorGamesMusicStomp-v0',
        'VNCArmorGamesMusicZap-v0',
        'VNCArmorGamesRhythmBlasterV2-v0',
        'VNCArmorGamesColorwars-v0',
        'VNCArmorGamesSpaceMadness-v0',
        'VNCArmorGamesHyperTravel-v0',
        'VNCArmorGamesVelocity-v0',
        'VNCArmorGamesShortCircuit-v0',
        'VNCArmorGamesInfinitix-v0',
        'VNCArmorGamesRetron-v0',
        'VNCArmorGamesPaintWars-v0',
        'VNCArmorGamesGalaxyDefender-v0',
        'VNCArmorGamesNook-v0',
        'VNCArmorGamesKinetikz3-v0',
        'VNCArmorGamesKinetikz2-v0',
        'VNC2pgSmashTheSwine-v0',
        'VNC2pgBalloonGods-v0',
        'VNC2pgMiceVsHammers-v0',
        'VNCGamesButlerSheepster-v0',
        'VNCGamesButlerBlacksmithLab-v0',
        'VNCGamesButlerBusinessmanSimulator-v0',
        'VNC2pgGroundBattles-v0',
        'VNCArmorGamesRhythmSnake-v0',
        'VNCGamesButlerOldTv-v0',
        'VNCGamesButlerClickerMonsters-v0',
        'VNC2pgMightyTower-v0',
        'VNCArmorGamesAlienTransporter-v0',
        'VNCArmorGamesSheepy-v0',
        'VNCArmorGamesHalloweenJam-v0',
        'VNCArmorGamesCooliobeat-v0',
        'VNCArmorGamesFunkostroll-v0',
        'VNCArmorGamesDanceBattle-v0',
        'VNCGamesButlerEvilSun-v0',
        'VNC2pgTheTowerman-v0',
        'VNCNotDopplerDotsRevamped-v0',
        'VNCNotDopplerDots-v0',
        'VNCArmorGamesScribble2-v0',
        'VNCArmorGamesScribble-v0',
        'VNCArmorGamesSliceTheBox-v0',
        'VNCArmorGamesTattooArtist-v0',
        'VNC1000WebGamesBigWheelsTrial-v0',
        'VNCGamesButlerSuperRallyChallenge2-v0',
        'VNCArmorGamesSushiCatTheHoneymoon-v0',
        'VNC2pgSuperShinyheadHarderThanFlappyBird-v0',
        'VNCY8BalloonHero-v0',
        'VNC1000WebGamesAircraftRace-v0',
        'VNC1000WebGamesPlaneRace-v0',
        'VNC1000WebGamesPlaneRace2-v0',
        'VNCNotDopplerSkyQuest-v0',
        'VNCY8StarCars-v0',
        'VNCGamesButlerGravityBall-v0',
        'VNCArmorGamesHelicopsTerritories-v0',
        'VNCArmorGamesPowerCopter-v0',
        'VNCArmorGamesFiveTil-v0',
        'VNCArmorGamesHeliVsTower-v0',
        'VNC2pgPunchBallJump-v0',
        'VNC2pgGhostClimb2Player-v0',
        'VNCArmorGamesSpinClimbGreen-v0',
        'VNCArmorGamesQubeyTheCube-v0',
        'VNCGamesButlerSantaClimbHere-v0',
        'VNCGamesButlerFluffRush-v0',
        'VNCArmorGamesBurgerBar-v0',
        'VNCGamesButlerXmasChains-v0',
        'VNCArmorGamesPlopPlopLite-v0',
        'VNCGamesButlerHexBattles-v0',
        'VNCNotDopplerLineGameLimeEdition-v0',
        'VNCArmorGamesOddball2-v0',
        'VNC1000WebGamesTankStorm4-v0',
        'VNCGamesButlerRushOfTanks-v0',
        'VNCGamesButlerDigToChina-v0',
        'VNCArmorGamesStratega-v0',
        'VNC1000WebGamesGalleonFight-v0',
        'VNCNotDopplerLessQuick-v0',
        'VNCNotDopplerQuick-v0',
        'VNC1000WebGamesBikeTrial4-v0',
        'VNC1000WebGamesBikeTrial3-v0',
        'VNC1000WebGamesBikeTrial2-v0',
        'VNC1000WebGamesRapidGun-v0',
        'VNC1000WebGamesBikeTrial-v0',
        'VNC2pgBugsGotGuns-v0',
        'VNCArmorGamesHash-v0',
        'VNC1000WebGamesOkParking-v0',
        'VNCGamesButlerLaxAirbusParking-v0',
        'VNC1000WebGamesHungryLittlePenguins-v0',
        'VNC1000WebGamesFirefighterCannon-v0',
        'VNCGamesButlerMummyMadness-v0',
        'VNCGamesButlerPiratesAndCannons-v0',
        'VNCGamesButlerSaveTheDummyHolidays-v0',
        'VNCGamesButlerClimbOrDrown2-v0',
        'VNCGamesButlerPaulVaulting-v0',
        'VNCGamesButlerWishTotemsLevelPack-v0',
        'VNCGamesButlerKingRolla-v0',
        'VNCGamesButlerWishTotems-v0',
        'VNCGamesButlerReleaseTheMooks3-v0',
        'VNCGamesButlerMushboomsLevelPack2-v0',
        'VNCGamesButlerBlastTheMooksLevelPack-v0',
        'VNCGamesButlerBlastTheMooks-v0',
        'VNCGamesButlerMushboomsLevelPack-v0',
        'VNCGamesButlerMushbooms-v0',
        'VNCGamesButlerNeopods-v0',
        'VNCGamesButlerReleaseTheMooks2-v0',
        'VNCGamesButlerFrozenImps-v0',
        'VNCGamesButlerFlyAwayRabbit2-v0',
        'VNCGamesButlerReleaseTheMooks-v0',
        'VNCGamesButlerCatchTheStar-v0',
        'VNCGamesButlerMichimind-v0',
        'VNCGamesButlerJumprunner-v0',
        'VNCNotDopplerNumz-v0',
        'VNCNotDopplerMagicSafari-v0',
        'VNCNotDopplerEpicTimePirates-v0',
        'VNCArmorGamesParallelLevels-v0',
        'VNCGamesButlerMonsterLabFeedThemAll-v0',
        'VNCGamesButlerGameInit-v0',
        'VNC1000WebGamesHappyBallz-v0',
        'VNCArmorGamesGridShift-v0',
        'VNCArmorGamesSliceTheBoxRemaster-v0',
        'VNCKongregateFiller2-v0',
        'VNCKongregateFiller-v0',
        'VNCKongregatePathillogical-v0',
        'VNCArmorGamesSiegerRebuiltToDestroy-v0',
        'VNCArmorGamesSiegeHeroPiratePillage-v0',
        'VNCArmorGamesClaustrophobiumFourStepsFromDeath-v0',
        'VNCY8IsoblockerMaster-v0',
        'VNCY8Blix-v0',
        'VNCGamesButlerDitloid-v0',
        'VNC2pgRacerKartz-v0',
        'VNC1000WebGamesAtvRide-v0',
        'VNC1000WebGamesBoatDrive-v0',
        'VNC1000WebGamesTractorTrial2-v0',
        'VNC1000WebGamesRoadRacing-v0',
        'VNC1000WebGamesAsphaltMadness-v0',
        'VNCGamesButlerSurfBuggy-v0',
        'VNCArmorGamesMindImpulse-v0',
        'VNC2pgPinataWarriors-v0',
        'VNCNotDopplerIntoSpace-v0',
        'VNCGamesButlerRocketBootsInc-v0',
        'VNCArmorGamesPhit-v0',
        'VNCY8CowboyVsUfos-v0',
        'VNC2pgShamelessClone2-v0',
        'VNCArmorGamesDontPanic-v0',
        'VNCArmorGamesPixelBasher-v0',
        'VNCArmorGamesBearInSuperActionAdventure-v0',
        'VNCArmorGamesPixelPurge-v0',
        'VNCArmorGamesTosuta-v0',
        'VNCArmorGamesAerorumble-v0',
        'VNCArmorGamesPixelFighta-v0',
        'VNC1000WebGamesTankStorm3-v0',
        'VNC1000WebGamesBulletFury-v0',
        'VNC1000WebGamesHeavyLegion2-v0',
        'VNC1000WebGamesTankStorm2-v0',
        'VNC1000WebGamesTankStorm-v0',
        'VNC2pgBubbleSlasher-v0',
        'VNC2pgGalacticCats-v0',
        'VNCNotDopplerRaze3-v0',
        'VNCNotDopplerBlosics3-v0',
        'VNCNotDopplerSundrops-v0',
        'VNCNotDopplerBlosics2LevelPack-v0',
        'VNCNotDopplerBlosics2-v0',
        'VNCArmorGamesBullets-v0',
        'VNCArmorGamesSuperXtreme5MinuteShootEmUp-v0',
        'VNCArmorGamesDualDimension-v0',
        'VNCArmorGamesPocketRocket-v0',
        'VNCArmorGamesKinetikz-v0',
        'VNCArmorGamesProjectMonochrome-v0',
        'VNCArmorGamesConjure-v0',
        'VNCArmorGamesStitchlandConflict-v0',
        'VNCArmorGamesPenguinSkate2-v0',
        'VNCArmorGamesGo-v0',
        'VNC1000WebGamesColorZapper-v0',
        'VNCGamesButlerJumpOverTheRings-v0',
        'VNCGamesButlerMonsterTruckRally-v0',
        'VNCGamesButlerCrapImBroke-v0',
        'VNCGamesButlerCrumbs2-v0',
        'VNCGamesButler30Seconds-v0',
        'VNCArmorGamesParachuteRetrospect-v0',
        'VNCY8LetsFall-v0',
        'VNCNotDopplerGluey2-v0',
        'VNCNotDopplerHotspot-v0',
        'VNCNotDopplerPolygonalFury-v0',
        'VNCNotDopplerPointer-v0',
        'VNCArmorGamesClusterobot-v0',
        'VNCArmorGamesCooliodj-v0',
        'VNCArmorGamesRhythmRockets-v0',
        'VNCArmorGamesFasterMiterMaster-v0',
        'VNCArmorGamesHammerBall-v0',
        'VNCArmorGamesChuteAcademy-v0',
        'VNCArmorGamesGrowbox-v0',
        'VNCArmorGamesBubbleBlubbs-v0',
        'VNCArmorGamesPyro-v0',
        'VNCArmorGamesCattlepultPlayerPack-v0',
        'VNCArmorGamesCattlepult-v0',
        'VNCArmorGamesSlingBaby-v0',
        'VNCArmorGamesSolarsaurs-v0',
        'VNC2pgSnakeFightArena-v0',
        'VNCY8GalaxyEvo2-v0',
        'VNCNotDopplerHarvest-v0',
        'VNCGamesButlerPowerSwing-v0',
        'VNC2pgFishAndDestroy-v0',
        'VNCArmorGamesMedievalShark-v0',
        'VNCArmorGamesAnywayFish-v0',
        'VNCArmorGamesJamesTheDeepSeaZebra-v0',
        'VNCY8TableTennisChallenge-v0',
        'VNCY8BoxBlocks-v0',
        'VNCGamesButlerSuperPuzzlePlatformer-v0',
        'VNC2pgNoughtsAndCrosses-v0',
        'VNC2pgNoughtsAndCrossesExtreme-v0',
        'VNC1000WebGamesMarsColonyTd-v0',
        'VNC1000WebGamesTowerEmpire2-v0',
        'VNC1000WebGamesTowerEmpire-v0',
        'VNC1000WebGamesWildWestConflict-v0',
        'VNCArmorGames99BricksTheLegendOfGarry-v0',
        'VNC1000WebGames4x4Monster3-v0',
        'VNC1000WebGamesTractorTrial-v0',
        'VNCGamesButlerRussianTruck-v0',
        'VNCGamesButlerDrinkBeerNeglectFamily-v0',
        'VNC2pgDolphinVolleyball-v0',
        'VNCArmorGamesTypeasaurus-v0',
        'VNC1000WebGamesDriveToWreck3-v0',
        'VNC1000WebGamesDriveToWreck2-v0',
        'VNC1000WebGamesDriveToWreck-v0',
        'VNCGamesButlerMadpetSkateboarder2-v0',
        'VNCGamesButlerBackHome-v0',
        'VNCGamesButlerChockABox-v0',
        'VNCGamesButlerUdderChaos-v0',
        'VNCGamesButlerDeathDiceOverdose-v0',
        'VNCKongregateIcyGifts2-v0',
        'VNCKongregateHiredHeroes-v0',
        'VNCKongregateFlyingCookieQuest-v0',
        'VNCKongregateTrickyRick-v0',
        'VNCKongregateCatGodVsSunKing2-v0',
        'VNCKongregateTokyoGuineaPop-v0',
        'VNCKongregateEffingWorms-v0',
        'VNCKongregateStickBlender-v0',
        'VNCKongregateTheGreatSiege-v0',
        'VNCKongregateCaptainSteelbounce-v0',
        'VNCKongregateIceRun-v0',
        'VNCKongregateDoodleGod2Walkthrough-v0',
        'VNCKongregateEpicBattleFantasy4-v0',
        'VNCKongregatePuzzleMonsters-v0',
        'VNCKongregateRunRunRan-v0',
        'VNCKongregateNanoKingdoms2JokersRevenge-v0',
        'VNCKongregateStardrops-v0',
        'VNCKongregateFeedMeMoar-v0',
        'VNCKongregateCoasterRacer3-v0',
        'VNCKongregateConquerium-v0',
        'VNCKongregateNOfficialWebVersion-v0',
        'VNCKongregateNewSplitterPals-v0',
        'VNCKongregateTheBravestHunter-v0',
        'VNCKongregateEnhanced-v0',
        'VNCKongregateTtRacer-v0',
        'VNCKongregateCrystalStoryIi-v0',
        'VNCKongregateTapRocket-v0',
        'VNCKongregateLearnToFlyIdle-v0',
        'VNCKongregateHowDareYou-v0',
        'VNCKongregateWarOfTheShard-v0',
        'VNCKongregateFpaWorld1Remix-v0',
        'VNCKongregateStickyNinjaMissions-v0',
        'VNCKongregateCardinalQuest2-v0',
        'VNCKongregateBulletHeaven-v0',
        'VNCKongregateBulletHeaven2-v0',
        'VNCArmorGamesBeachCrazy-v0',
        'VNCArmorGamesJonnyBackflip-v0',
        'VNCArmorGamesParticleWarsExtreme-v0',
        'VNCArmorGamesFallDamage-v0',
        'VNCArmorGamesColorfill-v0',
        'VNCArmorGamesStargrazer-v0',
        'VNCArmorGamesDodge-v0',
        'VNCArmorGamesDropblox-v0',
        'VNCArmorGamesXChains-v0',
        'VNCArmorGamesXnake-v0',
        'VNCArmorGamesSpectrum-v0',
        'VNCArmorGamesKnightsOfRock-v0',
        'VNCArmorGamesSpectrumHeist-v0',
        'VNCY8ArkanoidGame-v0',
        'VNCY8Frogged-v0',
        'VNCY8TurtleBreak-v0',
        'VNCGames68QuashBoard-v0',
        'VNCGames68IdleFarmer-v0',
        'VNCGames68HoleInOne-v0',
        'VNCGames68Chefday-v0',
        'VNCGames68IdlePlanet-v0',
        'VNCGames68DeadEndSt-v0',
        'VNCGames68SuperBoxotron2000-v0',
        'VNCGames68AwesomeRun2-v0',
        'VNCGames68CoffeeClicker-v0',
        'VNCGames68TerrestrialConflict-v0',
        'VNCGames68HeroesOfMangaraTheFrostCrown-v0',
        'VNCGames68Stealthbound-v0',
        'VNCGames68FpaWorld1Remix-v0',
        'VNCGames68AspenSecret-v0',
        'VNCGames68LaserCannon3LevelsPack-v0',
        'VNCGames68MushyMishy-v0',
        'VNCGames68RiseOfChampions-v0',
        'VNCGames68FootballHeads201314Ligue1-v0',
        'VNCGames68Helixteus-v0',
        'VNCGames68DinoBubble-v0',
        'VNCGames68IdleChop-v0',
        'VNCGames68ClickerHeroes-v0',
        'VNCGames68Autoattack-v0',
        'VNCGames68MexicoRex-v0',
        'VNCGames68StealthboundLevelPack-v0',
        'VNCGames68InsaneCircle-v0',
        'VNCGames68TaxiInc-v0',
        'VNCGames68FlashsBounty-v0',
        'VNCGames68Flashcycle2-v0',
        'VNCGames68Madburger3-v0',
        'VNCGames68Sirtet-v0',
        'VNCGames68Raze3-v0',
        'VNCGames68EmpireBusiness2Beta-v0',
        'VNCGames68SuperIdleMaster-v0',
        'VNCGames68CitySiege3FubarLevelPack-v0',
        'VNCGames68MonkeyGoHappyNinjaHunt2-v0',
        'VNCGames68DragonFortress-v0',
        'VNCGames68AnimeClicker2-v0',
        'VNCGames68ZombieDemolisher3-v0',
        'VNCGames68DisasterWillStrikeUltimateDisaster-v0',
        'VNCGames68PapaLouie3WhenSundaesAttack-v0',
        'VNCGames68DoodleGodBlitz-v0',
        'VNCGames68PerilousJourney2-v0',
        'VNCGames68TrafficCollision-v0',
        'VNCGames68CruiseAdventure-v0',
        'VNCGames68CurveFever-v0',
        'VNCGames68Legor9-v0',
        'VNCGames68TheSilentPlanet-v0',
        'VNCGames68Gameinit-v0',
        'VNCGames68SwingTriangle-v0',
        'VNCGames68ZombiesVsBrains-v0',
        'VNCGames68HeroSimulator-v0',
        'VNCGames68FrozenIslandsNewHorizons-v0',
        'VNCGames68BlockysEscape-v0',
        'VNCGames68BuildBalance2-v0',
        'VNCGames68ThatRedButton-v0',
        'VNCGames68TheCaseOfScaryShadow-v0',
        'VNCGames68BoxingLiveRound2-v0',
        'VNCGames68InfectonatorSurvivorsAlphaDemo-v0',
        'VNCGames68Coloruid-v0',
        'VNCGames68MotoTrialMania-v0',
        'VNCGames68FarmRush-v0',
        'VNCGames68Zombidle-v0',
        'VNCGames68SpellIdle2-v0',
        'VNCGames68BlackAndWhiteEscapeTheOffice-v0',
        'VNCGames68BabyBelleAdoptAPet-v0',
        'VNCGames68WastelandSiege-v0',
        'VNCGames68AWeekendAtTweetys-v0',
        'VNCGames68MazeEye-v0',
        'VNCGames68ToyWarAngryRobotDog-v0',
        'VNCGames68MarshmallowsEscape-v0',
        'VNCGames68SnackOnLittleCreatures-v0',
        'VNCGames68PacmanMazeY8-v0',
        'VNCGames68Stand-v0',
        'VNCGames68MasterDifference-v0',
        'VNCGames68CastleRush-v0',
        'VNCGames68WindowShooter-v0',
        'VNCGames68GardenRush-v0',
        'VNCGames68DotGrowth-v0',
        'VNCGames68DeadHungry2-v0',
        'VNCGames68ViewtifulFightClub2-v0',
        'VNCGames68FreeSouls-v0',
        'VNCGames68ParkingFury-v0',
        'VNCGames68AchilliaTheGame-v0',
        'VNCGames68GamerMemoryTest-v0',
        'VNCGames68BloodyMonstersPack2-v0',
        'VNCGames68MysticalAncientTreasure-v0',
        'VNCGames68MushroomCommando-v0',
        'VNCGames68MissionEscapeTheDojo-v0',
        'VNCGames68LonelyEscapeAsylum-v0',
        'VNCGames68Sieger2LevelPack-v0',
        'VNCGames68ToonEscapeSpookHouse-v0',
        'VNCGames68WhatsInsideTheBox-v0',
        'VNCGames68SavingLittleAlien-v0',
        'VNCGames68BalloonsPop-v0',
        'VNCGames68HoldTheFort-v0',
        'VNCGames68ToonEscapeMaze-v0',
        'VNCGames68PyramidApocalypse-v0',
        'VNCGames68AuroraRealMakeover-v0',
        'VNCGames68EuroKicks2016-v0',
        'VNCGames68IceCreamFromSpace-v0',
        'VNCGames68Krome-v0',
        'VNCGames68TheBigEscape-v0',
        'VNCGames68ShootTheCircle-v0',
        'VNCGames68VolcanoPanicInIsland-v0',
        'VNCGames68Business-v0',
        'VNCGames68BubbleRubbleTheIsland-v0',
        'VNCGames68InfernalMess-v0',
        'VNCGames68TrollfaceQuest13-v0',
        'VNCGames68VanguardWars-v0',
        'VNCGames68RobotDuelFight-v0',
        'VNCGames68TheOneForkRestaurantDx-v0',
        'VNCGames68WackyStrike-v0',
        'VNCGames68AmigoPanchoInAfghanistan-v0',
        'VNCGames68EnterTheDungeonGrabTheTreasureAndBewareTheDangers-v0',
        'VNCGames68BlackInk-v0',
        'VNCGames68TheCrimeReportsTheLockedRoomEpisode2-v0',
        'VNCGames68KitchenRestaurantCleanUp-v0',
        'VNCGames68SneakyScubaEscape-v0',
        'VNCGames68PonyClicker-v0',
        'VNCGames68IndependenceDaySlacking2015-v0',
        'VNCGames68WarHeroes-v0',
        'VNCGames68Crazycle-v0',
        'VNCGames68DinoMeatHunt3Extra-v0',
        'VNCGames68Paintwars-v0',
        'VNCGames68FindTheCandy3Kids-v0',
        'VNCGames68DisasterWillStrikeDefender-v0',
        'VNCGames68KangoIslands-v0',
        'VNCGames68WarBerlinIdle-v0',
        'VNCGames68PurifyTheLegendOfZ-v0',
        'VNCGames68Skytrip-v0',
        'VNCGames68Indefinite-v0',
        'VNCGames68MidnightMiner-v0',
        'VNCGames68IdleLifting-v0',
        'VNCGames68TrollingLionJump-v0',
        'VNCGames68IncrementalAcceleration-v0',
        'VNCGames68SpanishLiga2016-v0',
        'VNCGames68NightDrivin-v0',
        'VNCGames68SurvivorMissionD-v0',
        'VNCGames68FreecellDuplex-v0',
        'VNCGames68LlamasInDistress-v0',
        'VNCGames68CoverOrangeJourneyGangsters-v0',
        'VNCGames68BubbleAdventures-v0',
        'VNCGames68RabbitPlanetEscape-v0',
        'VNCGames68BunnyAndSquirt-v0',
        'VNCGames68Gloom-v0',
        'VNCGames68FireworksGame-v0',
        'VNCGames68VolleyBomb-v0',
        'VNCGames68PigDestroyer-v0',
        'VNCGames68UltimateLegend-v0',
        'VNCGames68SuperBomb-v0',
        'VNCGames68AssembleBots-v0',
        'VNCGames68MonsterChains-v0',
        'VNCGames68AbductionGrannysVersion-v0',
        'VNCGames68OswaldTheAngryDwarf-v0',
        'VNCGames68HunterForDismantlers-v0',
        'VNCGames68BouncyCannon-v0',
        'VNCGames68PouThanksgivingDaySlacking-v0',
        'VNCGames68AnotherLife2-v0',
        'VNCGames68GsSoccerWorldCup-v0',
        'VNCGames68BombThePiratePigs-v0',
        'VNCGames68ElClassico-v0',
        'VNCGames68TmntTurtlesInTime-v0',
        'VNCGames68SuperAdventurePalsBattleArena-v0',
        'VNCGames68JelliesFun-v0',
        'VNCGames68SuperBattleCity2-v0',
        'VNCGames68RingsideHero-v0',
        'VNCGames68AlchemySwap-v0',
        'VNCGames68Cleopatra-v0',
        'VNCGames68SuperBomberman2-v0',
        'VNCGames68Contra3TheAlienWars-v0',
        'VNCKongregateNotepadSnake-v0',
]:
    register(
        id=game,
        entry_point='gym_vnc.wrappers:WrappedVNCFlashgamesEnv',
        tags={
            'vnc': True,
            'flashgames': True,
            'runtime': 'vnc-flashgames',
            'metadata_encoding': metadata_v1,
            'action_probe': {
                'type': 'key',
                'value': 0x60,
            }
        },
        timestep_limit=20000,
    )

register(
    id='VNCNoopFlashgamesEnv-v0',  # Special noop flashgame env
    entry_point='gym_vnc.vnc:WrappedVNCFlashgamesEnv',
    tags={
        'vnc': True,
        'flashgames': True,
        'runtime': 'vnc-flashgames',
    },
    timestep_limit=10**7,
)

# VNCWorldOfBits
# primitive browser tasks.
vnc_world_of_bits = [
    'VNCMiniWorldOfBits-v0',
    'VNCClickCollapsible-v0',
    'VNCClickCollapsible2-v0',
    'VNCClickDialog-v0',
    'VNCClickDialog2-v0',
    'VNCClickLink-v0',
    'VNCClickButton-v0',
    'VNCClickButtonSequence-v0',
    'VNCClickCheckboxes-v0',
    'VNCClickOption-v0',
    'VNCClickPie-v0',
    'VNCClickTab-v0',
    'VNCClickTab2-v0',
    'VNCClickTest-v0',
    'VNCClickTest2-v0',
    'VNCClickWidget-v0',

    'VNCChaseCircle-v0',
    'VNCChooseDate-v0',
    'VNCChooseList-v0',
    'VNCClickMenu-v0',
    'VNCClickMenu2-v0',
    'VNCClickScrollList-v0',
    'VNCDragBox-v0',
    'VNCDragItems-v0',
    'VNCDragItemsGrid-v0',
    'VNCDragSortNumbers-v0',
    'VNCGuessNumber-v0',
    'VNCHighlightText-v0',
    'VNCHighlightText2-v0',
    'VNCNavigateTree-v0',
    'VNCResizeTextarea-v0',
    'VNCSimonSays-v0',
    'VNCUseSpinner-v0',
    'VNCUseSlider-v0',
    'VNCUseSlider2-v0',
    'VNCSocialMedia-v0',
    'VNCUseAutocomplete-v0',

    'VNCClickColor-v0',
    'VNCClickShades-v0',
    'VNCClickShape-v0',
    'VNCCountShape-v0',
    'VNCCountSides-v0',
    'VNCDragCube-v0',
    'VNCDragShapes-v0',
    'VNCIdentifyShape-v0',
    'VNCUseColorwheel-v0',
    'VNCUseColorwheel2-v0',

    'VNCCopyPaste-v0',
    'VNCCopyPaste2-v0',
    'VNCEnterDate-v0',
    'VNCEnterPassword-v0',
    'VNCEnterText-v0',
    'VNCEnterText2-v0',
    'VNCEnterTextDynamic-v0',
    'VNCEnterTime-v0',
    'VNCFindWord-v0',
    'VNCFocusText-v0',
    'VNCFocusText2-v0',
    'VNCLoginUser-v0',
    'VNCNumberCheckboxes-v0',
    'VNCReadTable-v0',
    'VNCReadTable2-v0',
    'VNCScrollText-v0',
    'VNCScrollText2-v0',
    'VNCSearchEngine-v0',
    'VNCTextTransform-v0',
]
# signup forms.
for _id in range(20):
    vnc_world_of_bits.append('VNCSignup-{}-v0'.format(_id))

for _site in ['aircanada', 'jetblue', 'kayak', 'aa', 'virginamerica', 'frontier',
               'united', 'interjet', 'southwest', 'delta', 'airchina', 'suncountry',
               'allegiantair', 'airfrance', 'ctrip', 'westjet', 'alaska']:
    vnc_world_of_bits.append('VNCRealWoB-BookFlight-{}-v0'.format(_site))

for _site in ['airfrance', 'craigslist', 'chase']:
    vnc_world_of_bits.append('VNCRealWoB-ClickButton-{}-v0'.format(_site))

for game in vnc_world_of_bits:
    register(
        id=game,
        entry_point='gym_vnc.wrappers:WrappedVNCEnv',
        tags={
            'vnc': True,
            'wob': True,
            'runtime': 'vnc-world-of-bits'
        },
        timestep_limit=10**7,
    )

# Minecraft
minecraft = {
    'VNCMinecraftDefaultWorld1-v0': 'default_world_1.xml',
    'VNCMinecraftDefaultFlat1-v0': 'default_flat_1.xml',
    'VNCMinecraftTrickyArena1-v0': 'tricky_arena_1.xml',
    'VNCMinecraftEating1-v0': 'eating_1.xml',
    'VNCMinecraftCliffWalking1-v0': 'cliff_walking_1.xml',
    'VNCMinecraftMaze1-v0': 'maze_1.xml',
    'VNCMinecraftMaze2-v0': 'maze_2.xml',
    'VNCMinecraftBasic-v0': 'basic.xml',
    'VNCMinecraftObstacles-v0': 'obstacles.xml',
    'VNCMinecraftSimpleRoomMaze-v0': 'simpleRoomMaze.xml',
    'VNCMinecraftAttic-v0': 'attic.xml',
    'VNCMinecraftVertical-v0': 'vertical.xml',
    'VNCMinecraftComplexityUsage-v0': 'complexity_usage.xml',
    'VNCMinecraftMedium-v0': 'medium.xml',
    'VNCMinecraftHard-v0': 'hard.xml'
}

for game, file in minecraft.items():
    register(
        id=game,
        entry_point='gym_minecraft.envs:MinecraftEnv',
        kwargs={'mission_file': file},
        tags={
            'vnc': True,
            'minecraft': True,
            'runtime': 'vnc-minecraft'
        },
        timestep_limit=10**7,
    )

# VNCStarCraft
for id in ['starcraft.TerranAstralBalance-v0']:
    register(
        id=id,
        entry_point='gym_vnc.wrappers:WrappedVNCStarCraftEnv',
        tags={
            'vnc': True,
            'starcraft': True,
            'runtime': 'vnc-starcraft',
        },
        timestep_limit=10**7,
    )

# VNCGTAV
for gtav_game in ['VNCGTAV-v0', 'VNCGTAVSpeed-v0', 'VNCGTAVWinding-v0']:
    register(
        id=gtav_game,
        entry_point='gym_vnc.wrappers:WrappedVNCGTAVEnv',
        tags={
            'vnc': True,
            'gtav': True,
            'runtime': 'vnc-windows',
        },
        timestep_limit=10**7,
    )

# VNC World of Goo
# TODO: move this out into separate registry -- like flashgames has
register(
    id='VNCWorldOfGoo-GoingUp-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCWorldOfGooEnv',
    tags={
        'vnc': True,
        'wog': True,
        'runtime': 'vnc-world-of-goo',
    },
    timestep_limit=10**7,
)

# VNCInternet-v0
register(
    id='VNCSlitherIO-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCInternetEnv',
    tags={
        'vnc': True,
        'internet': True,
        'slither': True,
        'runtime': 'vnc-flashgames',
        'metadata_encoding': metadata_v1,
        'action_probe': {
            'type': 'key',
            'value': 0x60,
        }
    },
    timestep_limit=10**7,
)

########## Old games; many of which we don't have the orights to distribute.
#
# https://docs.google.com/spreadsheets/d/1E8aKQtEnVoHO3f17-mIYcv8JpeV8UoV3imqr_xphP1o/edit#gid=0 has the exact permissions list
for game in ['VNC42Game-v0', 'VNCAirBattle-v0', 'VNCAmberialAxis-v0',
             'VNCAsteroidCrash-v0', 'VNCAthletics-v0', 'VNCAvalancher-v0',
             'VNCAvatarElementalEscape-v0', 'VNCBowAdventure-v0', 'VNCCanopy-v0',
             'VNCCaveman-v0', 'VNCChronotron-v0', 'VNCCommunityCollegeSim-v0',
             'VNCDannyPhantom-v0', 'VNCDirkValentine-v0',
             'VNCDonkeyKongReturns-v0', 'VNCDoubleEdged-v0',
             'VNCEnoughPlumbers2-v0', 'VNCEscapeTheRedGiant-v0', 'VNCFat-v0',
             'VNCFinalCommando-v0', 'VNCFirebug-v0', 'VNCFlagman-v0',
             'VNCFloodRunner4-v0', 'VNCFlubberRise-v0', 'VNCFrogDares-v0',
             'VNCGSwitch-v0', 'VNCGravinaytor-v0', 'VNCGuitarManiac-v0',
             'VNCGunpowderAndFeathers-v0', 'VNCHeavyPawnage-v0',
             'VNCHelicopter-v0', 'VNCIndestructoTank-v0', 'VNCIndianaJones-v0',
             'VNCJetpacTheRemake-v0', 'VNCJimmyJumper-v0', 'VNCKillbot-v0',
             'VNCKillme-v0', 'VNCLeapOfFaith-v0', 'VNCLemmingsReturns-v0',
             'VNCLittleLoki-v0', 'VNCMalichite-v0', 'VNCMarioCatcher2-v0',
             'VNCMarioCombat-v0', 'VNCMarioTimeAttack-v0',
             'VNCMatrixBulletTime-v0', 'VNCMetroSiberia-v0', 'VNCMonkeyManic-v0',
             'VNCMonolithsMarioWorld2-v0', 'VNCMonsterEvolution-v0', 'VNCMoss-v0',
             'VNCMotherLoad-v0', 'VNCMultitask-v0', 'VNCNanowar-v0',
             'VNCNinjaCat-v0', 'VNCOfficeTrap-v0', 'VNCOneAndOneStory-v0',
             'VNCOneButtonBob-v0', 'VNCOozingForever-v0', 'VNCPacmanPlatform2-v0',
             'VNCPandemonium-v0', 'VNCPapaLouie-v0', 'VNCPixelKnight2-v0',
             'VNCPortalFlash-v0', 'VNCPowerFox4-v0', 'VNCPowerRangers-v0',
             'VNCPrimary-v0', 'VNCRabbitRustler-v0', 'VNCRainbow-v0',
             'VNCRangeman-v0', 'VNCReachForTheSky-v0', 'VNCRevertToGrowth2-v0',
             'VNCRobotAdventure-v0', 'VNCRobotWantsFishy-v0', 'VNCRocket-v0',
             'VNCRocketCar-v0', 'VNCRoverArcher-v0', 'VNCRubbleRacer-v0',
             'VNCRun3-v0', 'VNCSantasDeepFreeze-v0', 'VNCSavingTheCompany-v0',
             'VNCSkyIsland-v0', 'VNCSleepyStusAdventure-v0', 'VNCSnowTrouble-v0',
             'VNCSonicFlash-v0', 'VNCSpaceIsKey-v0', 'VNCSpacemanAce-v0',
             'VNCSuperMario-v0', 'VNCSuperMarioSunshine64-v0',
             'VNCSuperSmashFlash2-v0', 'VNCSurvivalLab-v0', 'VNCTankWars-v0',
             'VNCTimeForCat-v0', 'VNCTinyCastle-v0', 'VNCTinySquad-v0',
             'VNCUnfinishedShadowGame-v0', 'VNCViridia-v0',
             'VNCZombieKnight-v0']:
    register(
        id=game,
        entry_point='gym_vnc.wrappers:WrappedVNCFlashgamesEnv',
        tags={
            'vnc': True,
            'flashgames': True,
            'runtime': 'vnc-flashgames',
        },
        timestep_limit=10**7,
    )
