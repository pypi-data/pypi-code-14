from csgo.enums import ECsgoGCMsg

class Match(object):
    def __init__(self):
        super(Match, self).__init__()

        # register our handlers
        self.on(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchmakingGC2ClientHello, self.__handle_mmstats)
        self.on(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchList, self.__handle_match_list)
        self.on(ECsgoGCMsg.EMsgGCCStrike15_v2_WatchInfoUsers, self.__handle_watch_info)

    def request_matchmaking_stats(self):
        """
        Request matchmaking statistics

        Response event: ``matchmaking_stats``

        :param message: `CMsgGCCStrike15_v2_MatchmakingGC2ClientHello` proto message

        """
        self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchmakingClient2GCHello)

    def __handle_mmstats(self, message):
        self.emit("matchmaking_stats", message)

    def request_current_live_games(self):
        """
        Request current live games

        Response event: ``current_live_games``

        :param message: `CMsgGCCStrike15_v2_MatchList` proto message

        """
        self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestCurrentLiveGames)

    def request_live_game_for_user(self, account_id):
        """
        Request recent games for a specific user

        :param account_id: account id of the user
        :type account_id: :class:`int`

        Response event: ``live_game_for_user``

        :param message: `CMsgGCCStrike15_v2_MatchList` proto message

        """
        self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestLiveGameForUser, {
                    'accountid': account_id,
                 })

    def request_full_match_info(self, matchid, outcomeid, token):
        """
        Request full match info. The parameters can be decoded from a match ShareCode

        :param matchid: match id
        :type matchid: :class:`int`
        :param outcomeid: outcome id
        :type outcomeid: :class:`int`
        :param token: token
        :type token: :class:`int`

        Response event: ``full_match_info``

        :param message: `CMsgGCCStrike15_v2_MatchList` proto message
        """
        self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestFullGameInfo, {
                    'matchid': matchid,
                    'outcomeid': outcomeid,
                    'token': token,
                 })

    def request_recent_user_games(self, account_id):
        """
        Request recent games for a specific user

        :param account_id: account id of the user
        :type account_id: :class:`int`

        Response event: ``recent_user_games``

        :param message: `CMsgGCCStrike15_v2_MatchList` proto message

        """
        self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestRecentUserGames, {
                    'accountid': account_id,
                 })

    def __handle_match_list(self, message):
        emsg = message.msgrequestid

        if emsg == ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestCurrentLiveGames:
            self.emit("current_live_games", message)
        elif emsg == ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestLiveGameForUser:
            self.emit("live_game_for_user", message)
        elif emsg == ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestRecentUserGames:
            self.emit("recent_user_games", message)
        elif emsg == ECsgoGCMsg.EMsgGCCStrike15_v2_MatchListRequestFullGameInfo:
            self.emit("full_match_info", message)


    def request_watch_info_friends(self):
        """
        Request watch info for friends

        Response event: ``watch_info``

        :param message: `CMsgGCCStrike15_v2_WatchInfoUsers` proto message

        """
        self.send(ECsgoGCMsg.EMsgGCCStrike15_v2_ClientRequestWatchInfoFriends2)

    def __handle_watch_info(self, message):
        self.emit("watch_info", message)
