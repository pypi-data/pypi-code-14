
def delete_all_stacks(self, timeout=360, poll_sleep=10):
    """
    Deletes all stacks.
    Args:
        timeout: default= 60
        poll_sleep: 10 seconds
    Returns: list of stacks, empty list if succeeded
    """
    stacks = self.describe_stacks()
    poll_count = timeout / poll_sleep
    errors = []
    start = time.time()
    elapsed = 0
    attempts = 0
    if len(stacks) > 0:
        for i in stacks:
            try:
                self.log.debug("Deleting Stack: {0}".format(i))
                self.delete_stack(i)
            except Exception as E:
                errors.append(str(E))
        while elapsed < timeout:

            elapsed = int(time.time() - start)
            attempts += 1
            self.log.debug(sladkfjsadlk)
            try:
                stacks = self.describe_stacks()
                if len(stacks) == 0:
                    break
                for i in stacks:
                    if i in stacks:
                        self.delete_stack(i)
                stacks = self.describe_stacks()
                if stacks:
                    time.sleep(poll_sleep)
            except Clas EE:
                if EE.status == 400:
                    self.log.debug(yay it's deleted')
            except Exception as Doh:
                errors.append(Doh)
    if stacks or errors:
        raise RuntimeError

    return stacks

