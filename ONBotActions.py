from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from operator import attrgetter

class ONBotActions(UserActionsBase):
    """ Actions for controlling ONB robot/live set. """

    def create_actions(self):
        self.add_global_action('cue', self.cue_next_action)
        self.add_global_action('lfu', self.loop_from_until_action)

    def cue_next_action(self, action_def, args):
        """ Stops playback and moves the insert marker to the next cue point. """
        song = self.song()
        song.stop_playing()
        for cue in sorted(song.cue_points, key=attrgetter('time')):
            if cue.time > song.current_song_time:
                self.canonical_parent.clyphx_pro_component.trigger_action_list('wait 2 ; loc "%s"' % cue.name)
                break

    def loop_from_until_action(self, action_def, args):
        """ Turns on looping for the specified duration starting at the given position. """
        clyph = self.canonical_parent.clyphx_pro_component
        parts = args.split()
        clyph.trigger_action_list('loop %s ; loop >%s ; loop on' % (parts[1], parts[0]))