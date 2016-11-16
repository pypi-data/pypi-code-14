from gym_vnc import error
import six

def merge_infos(info1, info2):
    """We often need to aggregate together multiple infos. Most keys can
    just be clobbered by the new info, but e.g. any keys which contain
    counts should be added. The merge schema is indicated by the key
    namespace.

    Namespaces:

    - stats.timers: Timing
    - stats.gauges: Gauge values
    - stats.*: Counts of a quantity
    """
    for key, value in six.iteritems(info2):
        if key in info1 and key.startswith('stats'):
            if key.startswith('stats.timers'):
                # timer
                info1[key] += value
            elif key.startswith('stats.gauges'):
                # gauge
                info1[key] = value
            else:
                # counter
                info1[key] += value
        else:
            info1[key] = value

def merge_reward_n(accum_reward_n, reward_n):
    for i in range(len(reward_n)):
        if reward_n[i] is not None:
            # Add rewards
            accum_reward_n[i] += reward_n[i]

def merge_n(
        accum_reward_n, accum_done_n, accum_info,
        reward_n, done_n, info,
):
    for i in range(len(reward_n)):
        if reward_n[i] is not None:
            # Add rewards
            accum_reward_n[i] += reward_n[i]
        # Set done if any are done
        if done_n[i]:
            accum_done_n[i] = done_n[i]

    # Merge together infos. We deep merge the 'n' key and do a
    # simple merge on everything else.
    accum_info_n = accum_info['n']
    for accum_info_i, info_i in zip(accum_info_n, info['n']):
        merge_infos(accum_info_i, info_i)

    merge_infos(accum_info, info)
    accum_info['n'] = accum_info_n
