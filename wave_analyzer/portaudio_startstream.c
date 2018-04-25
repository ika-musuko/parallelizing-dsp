static PaError StartStream( PaStream *s )
{
    PaError result = paNoError;
    PaAlsaStream* stream = (PaAlsaStream*)s;
    int streamStarted = 0;  /* So we can know whether we need to take the stream down */

    /* Ready the processor */
    PaUtil_ResetBufferProcessor( &stream->bufferProcessor );

    /* Set now, so we can test for activity further down */
    stream->isActive = 1;

    if( stream->callbackMode )
    {
        /* create a new thread with the defined stream_callback function (internally calls pthread_create()) */
        PA_ENSURE( PaUnixThread_New( &stream->thread, &CallbackThreadFunc, stream, 1., stream->rtSched ) );
    }
    else
    {
        PA_ENSURE( AlsaStart( stream, 0 ) );
        streamStarted = 1;
    }

end:
    return result;
error:
    if( streamStarted )
    {
        AbortStream( stream );
    }
    stream->isActive = 0;

    goto end;
}
