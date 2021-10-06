/**********************************************************************
** Copyright Eurocopter France 2009
** Author :  F. RUYSSEN
** Date of creation : 25/05/2009
** Module name : DelayWoId
** Description : Applies a DelayWoId of Time_constant/Time_period cycle on the input
** Requirements : LLR-DELAYWOID-001
**				  LLR-DELAYWOID-002
***********************************************************************
** History of modification :
** 
***********************************************************************/

/* Include */
#include "DelayWoId_fctext.h"

/**********************************************************************
** Purpose : DelayWoId_Init
***********************************************************************
** Parameters :
** I : none
** O : _C_DelayWoId * DelayStruct
** I/O    : none
** Return : none
***********************************************************************
** Initialization of state variables
***********************************************************************/
void DelayWoId_init (_C_DelayWoId * DelayStruct)
{
    _int sample_index;
                            
    DelayStruct->DelayWoId_data.first_run = true;
    DelayStruct->DelayWoId_data.time_constant_p = 0.0;
    DelayStruct->DelayWoId_data.position_in = 0;
    DelayStruct->DelayWoId_data.position_out = 0;
    for (sample_index = 0; sample_index < C_sample_number; sample_index++)
    {
        DelayStruct->DelayWoId_data.sample[sample_index] = 0.0;
    }
	
    DelayStruct->DelayWoId_data.DelayWoId_param_out_of_ranges = -1; 
}

/**********************************************************************
** NAME : DelayWoId                           
***********************************************************************
** Parameters :                                                        
** I : none
** O : none
** I/O : _C_DelayWoId * DelayStruct
** Return : none
***********************************************************************
** Applies a DelayWoId of Time_constant/Time_period cycle on the input 
************************************************************************/
int DelayWoId(_C_DelayWoId * DelayStruct) {
    _int duration;
    _int LoopIndex;

	/* if previous time constant different from current time constant */
    if (DelayStruct->DelayWoId_data.time_constant_p != DelayStruct->_I1_Time_constant)
    {

        /* Time constant and Time period must be positive */
        if ((DelayStruct->_I1_Time_constant >= 0.0) && (DelayStruct->_I3_Time_Period > 0.0 ))
        {
			duration = (_int)( DelayStruct->_I1_Time_constant / DelayStruct->_I3_Time_Period + (real)(0.5));
			
			/* If duration is less than the sample number */
			if (duration < C_sample_number)
			{
				/* Save the current time constant */
				DelayStruct->DelayWoId_data.time_constant_p = DelayStruct->_I1_Time_constant;
				/* Compute the new position out */
				DelayStruct->DelayWoId_data.position_out = DelayStruct->DelayWoId_data.position_in - duration;
				
				if (DelayStruct->DelayWoId_data.position_out < 0)
				{
					/* Add the sample number to position out if its negative */
					DelayStruct->DelayWoId_data.position_out = C_sample_number + DelayStruct->DelayWoId_data.position_out;
				}
			}
			else
			{
				/* Parameters out of range, no update */
				DelayStruct->DelayWoId_data.DelayWoId_param_out_of_ranges = 1;
			} /* end of if ((duration < C_sample_number) */
        }
        else
        {
            /* Parameters out of range, no update */
            DelayStruct->DelayWoId_data.DelayWoId_param_out_of_ranges = 1;
        } /* end of if (( DelayStruct->_I1_Time_constant >= 0.0 ) && ( DelayStruct->_I3_Time_Period > 0.0 )) */

    } /* end (DelayStruct->DelayWoId_data.time_constant_p != DelayStruct->_I1_Time_constant) */


    if (DelayStruct->_I2_Re_init || DelayStruct->DelayWoId_data.first_run)
    {
        /* Initialization after Reinit or during the 1st call. */  
        for (LoopIndex = 0; LoopIndex < C_sample_number; LoopIndex++)
        {
            DelayStruct->DelayWoId_data.sample[LoopIndex] = DelayStruct->_I4_Output_Option;
        }

        DelayStruct->_O0_Output = DelayStruct->_I4_Output_Option;
        DelayStruct->DelayWoId_data.first_run = false;
    }

	/* Operational cyclical treatment  */
    if (!DelayStruct->_I2_Re_init)
    {
        /* note: taking into account DelayStruct->_I0_Input must be made before the release */
        /* (case of null DelayWoId)    */
		if ((DelayStruct->DelayWoId_data.position_in >= 0) && (DelayStruct->DelayWoId_data.position_in < C_sample_number))
		{
			DelayStruct->DelayWoId_data.sample[DelayStruct->DelayWoId_data.position_in] = DelayStruct->_I0_Input;
		}
		
		else
		{
			/* Should not happend, will write outside table, could led to unpredictable behavior */
            return EXIT_FAILURE;
		}
		
		/* If position_in is outside the limit */
        if (DelayStruct->DelayWoId_data.position_in < (C_sample_number - 1))
        {
            DelayStruct->DelayWoId_data.position_in++;
        }
        else
        {
            DelayStruct->DelayWoId_data.position_in = 0;
        }
	
		/* Must not read outside the sample array */
		if ((DelayStruct->DelayWoId_data.position_out >= 0) && (DelayStruct->DelayWoId_data.position_out < C_sample_number))
		{
			DelayStruct->_O0_Output = DelayStruct->DelayWoId_data.sample[DelayStruct->DelayWoId_data.position_out];
		}
		
		else
		{
			/* Should not happend, unpredictable value will be used, stop execution */
            return EXIT_FAILURE;
		}
		
		/* If position_out is outside the limit */
        if (DelayStruct->DelayWoId_data.position_out < (C_sample_number - 1))
        {
            DelayStruct->DelayWoId_data.position_out++;
        }
        else
        {
            DelayStruct->DelayWoId_data.position_out = 0;
        }
    } /* end if ( ! DelayStruct->_I2_Re_init ) */
    return EXIT_SUCCESS;
}





