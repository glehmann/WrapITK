#! /usr/bin/python
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
try:
  import hashlib as md5
except:
  import md5
import time
import cPickle 
from pygccxml import utils
import config as cxx_parsers_cfg

def file_signature( filename ):
    if not os.path.isfile( filename ):
        return None
    if not os.path.exists( filename ):
        return None
    # Extend here to use md5 hash for signature
    # - This change allows duplicate autogenerated files to be recognized
    #return os.path.getmtime( source )
    sig = md5.new()
    f = file(filename,'r')
    sig.update(f.read())
    f.close()    
    return sig.hexdigest()

def configuration_signature( config ):
    """ Return a signature for a configuration (config_t)
        object.  This can then be used as a key in the cache.
        This method must take into account anything about
        a configuration that could cause the declarations generated
        to be different between runs.
    """
    sig = md5.new()
    if isinstance( config, cxx_parsers_cfg.gccxml_configuration_t ):
        sig.update(str(config.gccxml_path))
    sig.update(str(config.working_directory))
    if isinstance( config, cxx_parsers_cfg.gccxml_configuration_t ):
        sig.update(str(config.cflags))
    for p in config.include_paths:
        sig.update(str(p))
    for s in config.define_symbols:
        sig.update(str(s))
    for u in config.undefine_symbols:
        sig.update(str(u))    
    return sig.hexdigest()

class cache_base_t( object ):
    logger = utils.loggers.declarations_cache
    
    def __init__( self ):
        object.__init__(self)
        
    def flush(self):
        """ Flush (write out) the cache to disk if needed. """
        raise NotImplementedError()
        
    def update(self, source_file, configuration, declarations, included_files):
        """ Update cache entry.
        @param source_file: path to the C++ source file being parsed
        @param configuration: configuration used in parsing (config_t)
        @param declarations: declaration tree found when parsing
        @param included_files: files included by parsing.
        """
        raise NotImplementedError()    
        
    def cached_value(self, source_file, configuration):
        """ Return declarations we have cached for the source_file and configuration
            given.
        @param source_file: path to the C++ source file being parsed.
        @param configuration: configuration to use for parsing (config_t)
        """        
        raise NotImplementedError()

class record_t( object ):
    def __init__( self
                  , source_signature
                  , config_signature
                  , included_files
                  , included_files_signature
                  , declarations ):
        self.__source_signature = source_signature
        self.__config_signature = config_signature
        self.__included_files = included_files
        self.__included_files_signature = included_files_signature
        self.__declarations = declarations
        self.__was_hit = True # Track if there was a cache hit
    
    def _get_was_hit(self):
        return self.__was_hit
    def _set_was_hit(self, was_hit):
        self.__was_hit = was_hit
    was_hit = property( _get_was_hit, _set_was_hit )
    
    def key(self):
        return ( self.__source_signature, self.__config_signature)
    
    @staticmethod
    def create_key( source_file, configuration ):
        return ( file_signature(source_file)
                 , configuration_signature(configuration))                 
    
    def __source_signature(self):
        return self.__source_signature
    source_signature = property( __source_signature )
    
    def __config_signature(self):
        return self.__config_signature
    config_signature = property( __config_signature )
        
    def __included_files(self):
        return self.__included_files
    included_files = property( __included_files )
    
    def __included_files_signature(self):
        return self.__included_files_signature
    included_files_signature = property( __included_files_signature )
           
    def __declarations(self):
        return self.__declarations
    declarations = property( __declarations )   

class file_cache_t( cache_base_t ):   
    """ Cache implementation to store data in a pickled form in a file. 
        This class contains some cache logic that keeps track of which entries
        have been 'hit' in the cache and if an entry has not been hit then
        it is deleted at the time of the flush().  This keeps the cache from
        growing larger when files change and are not used again.        
    """

    def __init__( self, name ):
        """
        @param name: name of the cache file.
        """
        cache_base_t.__init__( self )       
        self.__name = name                              # Name of cache file
        self.__cache = self.__load( self.__name )       # Map record_key to record_t
        self.__needs_flushed = not bool( self.__cache ) # If empty then we need to flush        
        for entry in self.__cache.itervalues(): # Clear hit flags
            entry.was_hit = False
        
    @staticmethod
    def __load( file_name ):
        " Load pickled cache from file and return the object. "
        cache = None
        if os.path.exists( file_name ) and not os.path.isfile( file_name ):
            raise RuntimeError( 'Cache should be initialized with valid full file name' )
        if not os.path.exists( file_name ):
            file( file_name, 'w+b' ).close()
            return {}
        cache_file_obj = file( file_name, 'rb' )
        try:
            file_cache_t.logger.info( 'Loading cache file "%s".' % file_name )
            start_time = time.clock()
            cache = cPickle.load( cache_file_obj )            
            file_cache_t.logger.debug( "Cache file has been loaded in %.1f secs"%( time.clock() - start_time ) )
            file_cache_t.logger.debug( "Found cache in file: [%s]  entries: %s"
                               % ( file_name, len( cache.keys() ) ) )
        except Exception, error:
            file_cache_t.logger.exception( "Error occured while reading cache file: %s", error )
            cache_file_obj.close()
            file_cache_t.logger.info( "Invalid cache file: [%s]  Regenerating." % file_name )
            file(file_name, 'w+b').close()   # Create empty file
            cache = {}                       # Empty cache            
        return cache
        
    def flush(self):
        # If not marked as needing flushed, then return immediately
        if not self.__needs_flushed:
            self.logger.debug("Cache did not change, ignoring flush.")
            return
        
        # Remove entries that did not get a cache hit
        num_removed = 0
        for key in self.__cache.keys():
            if not self.__cache[key].was_hit:
                num_removed += 1
                del self.__cache[key]
        if num_removed > 0:
            self.logger.debug(  "There are %s removed entries from cache." % num_removed )
        # Save out the cache to disk
        cache_file = file( self.__name, 'w+b' )
        cPickle.dump( self.__cache, cache_file, cPickle.HIGHEST_PROTOCOL )
        cache_file.close()

    def update(self, source_file, configuration, declarations, included_files):
        """ Update a cached record with the current key and value contents. """
        record = record_t( source_signature=file_signature(source_file)
                           , config_signature=configuration_signature(configuration)
                           , included_files=included_files
                           , included_files_signature=map( file_signature, included_files)
                           , declarations=declarations 
                        )
        # Switched over to holding full record in cache so we don't have
        # to keep creating records in the next method.
        self.__cache[ record.key() ] = record
        self.__cache[ record.key() ].was_hit = True
        self.__needs_flushed = True
    
    def cached_value(self, source_file, configuration):
        """ Attempt to lookup the cached decls for the given file and configuration.
            If not found or signature check fails, returns None.
        """
        key = record_t.create_key(source_file, configuration)
        if not self.__cache.has_key( key ):
            return None
        record = self.__cache[key]
        if self.__is_valid_signature( record ):
            record.was_hit = True                  # Record cache hit
            return record.declarations
        else: #some file has been changed 
            del self.__cache[key]
            return None
        
    def __is_valid_signature( self, record ):
        # This is now part of key
        #if self.__signature( record.source_file ) != record.source_file_signature:
        #    return False
        for index, included_file in enumerate( record.included_files ):
            if file_signature( included_file ) != record.included_files_signature[index]:
                return False
        return True
        

class dummy_cache_t( cache_base_t ):
    def __init__( self ):
        cache_base_t.__init__(self)
        
    def flush(self):
        pass
        
    def update(self, source_file, configuration, declarations, included_files):
        pass
        
    def cached_value(self, source_file, configuration):
        return None
