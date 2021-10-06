/**********************************************************************
** Copyright Eurocopter France 2010
** Author : F. RUYSSEN
** Date of creation : 29/05/2009
** Module name : lint1
** Description : Linear interpolation 1 input
** Requirements : LLR-LINT1-001
**                LLR-LINT1-002 
***********************************************************************
** History of modification :
** 
***********************************************************************/

/* Includes */
#include "lint1_fctext.h"

/**********************************************************************
** Purpose : lint1
***********************************************************************
** Parameters :
** I      : none                   
** O      : none
** I/O    : _C_lint1 *lint1Struct
** Return : none
***********************************************************************
** Linear interpolation extract.  
***********************************************************************/                           
void lint1 (_C_lint1 *lint1Struct)
{
    real Slope;
    real PtRef_Val_Prev;
    real PtRef_Arg_Prev;
    _int Bound;
    real *Arg_ptr;
    real *Val_ptr;
    
    
    Bound = lint1Struct->_I1_The_Table->Bound - 1;
    
	/* if incorrect Inputs */
    if ((lint1Struct->_I0_The_Input <= lint1Struct->_I1_The_Table->Point_Arg._F0 ) || (Bound <= 0))
    {
        lint1Struct->_O0_The_Output = lint1Struct->_I1_The_Table->Point_Val._F0;
    }
    else
    {
		/* Bound shall not be greater than C_int_pol_vec_size - 1 */
        if (Bound > (C_int_pol_vec_size - 1))
        {
            Bound = C_int_pol_vec_size - 1;
        }
       
        Val_ptr = &lint1Struct->_I1_The_Table->Point_Val._F0;
        Arg_ptr = &lint1Struct->_I1_The_Table->Point_Arg._F0;

        if (lint1Struct->_I0_The_Input >= *(Arg_ptr + Bound)) 
        { 
            lint1Struct->_O0_The_Output = *(Val_ptr + Bound);
        }
		/* all other cases must lie between */
        else
        {   
            /*Ensure correct value of lint1Struct->Last_Index*/
            if ((lint1Struct->Last_Index < 1) || (lint1Struct->Last_Index > Bound))
            {
                lint1Struct->Last_Index = 1 ;
            }
        
            /* Find the segment where lint1Struct->_I0_The_Input lies */
            while (lint1Struct->_I0_The_Input > *(Arg_ptr + lint1Struct->Last_Index))
            {
                lint1Struct->Last_Index++;
            }
			
            while (lint1Struct->_I0_The_Input < *(Arg_ptr + lint1Struct->Last_Index))
            {
                lint1Struct->Last_Index--;
            }

            /* previous point: */
            PtRef_Arg_Prev = *(Arg_ptr + lint1Struct->Last_Index);
            PtRef_Val_Prev = *(Val_ptr + lint1Struct->Last_Index);
            
            Val_ptr = Val_ptr + lint1Struct->Last_Index + 1;
            Arg_ptr = Arg_ptr + lint1Struct->Last_Index + 1;
 
            Slope = (*(Val_ptr) - PtRef_Val_Prev) / (*(Arg_ptr) - PtRef_Arg_Prev);
            lint1Struct->_O0_The_Output = PtRef_Val_Prev + Slope * (lint1Struct->_I0_The_Input - PtRef_Arg_Prev);
        } /* end if (lint1Struct->_I0_The_Input >= *(Arg_ptr + Bound)) */

    } /* end if ((lint1Struct->_I0_The_Input <= lint1Struct->_I1_The_Table->Point_Arg._F0 ) || (Bound <= 0)) */
	
/* end lint1 */
}

/**********************************************************************
** Purpose : lint1_init
***********************************************************************
** Parameters :
** I      : none                    
** O      : _C_lint1 *lint1Struct
** I/O    : none
** Return : none
***********************************************************************
** Init Last Index.  
***********************************************************************/   
void lint1_init (_C_lint1 *lint1Struct)
{
    lint1Struct->Last_Index = 1;
}

