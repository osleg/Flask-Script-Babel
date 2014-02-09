# -*- coding: utf-8 -*-
import subprocess as sp
import shlex
from flask.ext.script import Manager

__author__ = 'Alex Kir'

manager = Manager(usage='Controlling generation and update of languages')


@manager.option('-l', '--lazy', dest='lazy', action='store_true', default=False, help='Use babel lazy extension')
@manager.option('-f', '--file', dest='tFile', default='messages.pot', help='.pot file with translation')
@manager.option('-c', '--config', dest='conf', default='babel.cfg', help='babel cfg file')
def extract(lazy=False, tFile='messages.pot', conf='babel.cfg'):
    """
    Extracting all strings marked with babel.gettext to messages.pot file in current directory
    """
    s = 'pybabel -vvv extract -F %s -k lazy_gettext -o %s .' if lazy else 'pybabel -vvv extract -F %s -o %s .'
    p = sp.call(shlex.split(s % (conf, tFile)))
    return p


@manager.option('-d', '--directory', dest='directory', default='translations',
                help='Directory where translations are saved')
@manager.option('-l', '--language', dest='lang', default=None,
                help='Specify language to create', required=True)
@manager.option('-f', '--file', dest='tFile', default='messages.pot', help='.pot file with translation')
def init(directory='translations', lang=None, tFile='messages.pot'):
    """
    initializing language translation and creating .po file, use this only once
    """
    if not lang:
        raise
    s = 'pybabel init -i %s -d %s -l %s' % (tFile, directory, lang)
    p = sp.call(shlex.split(s))
    return p


@manager.option('-d', '--directory', dest='directory', default='translations',
                help='Directory where translations saved')
@manager.option('-l', '--language', dest='lang', default=None,
                help='If only one language need compilation you can specify it with -l flag')
def compile(directory='translations', lang=None):
    """
    Compile translation file
    """
    s = 'pybabel compile -d %s' % directory
    if lang: s += ' -l %s' % lang
    p = sp.call(shlex.split(s))
    return p


@manager.option('-f', '--file', dest='tFile', default='messages.pot', help='.pot file with translation')
@manager.option('-d', '--directory', dest='directory', default='translations',
                help='Directory where translations saved')
@manager.option('-l', '--language', dest='lang', default=None,
                help='If only one language need compilation you can specify it with -l flag')
def update(directory='translations', tFile='messages.pot', lang=None):
    """
    updates .po file with new strings, use only this after first init
    """
    s = 'pybabel update -i %s -d %s' % (tFile, directory)
    if lang: s += ' -l %s' % lang
    p = sp.call(shlex.split(s))
    return p