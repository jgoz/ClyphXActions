from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
from operator import attrgetter

class ONBotActions(UserActionsBase):
    """ Actions for controlling ONB robot/live set. """

    def create_actions(self):
        self.add_global_action('cue', self.cue_next_action)
        self.add_global_action('lfu', self.loop_from_until_action)
        self.add_global_action('playloop', self.play_or_loop_toggle)

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

    def play_or_loop_toggle(self, action_def, args):
        """ Plays when stopped, or toggles loop on/off when playing. """
        song = self.song()
        clyph = self.canonical_parent.clyphx_pro_component
        if song.is_playing:
            clyph.trigger_action_list('loop')
        else:
            song.start_playing()
