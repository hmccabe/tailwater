public class BarcodeImage implements Cloneable 
{
   public static final int MAX_HEIGHT = 30;
   public static final int MAX_WIDTH = 65;
   private boolean[][] image_data;
   
   public BarcodeImage()
   {
      this.image_data = new boolean[MAX_HEIGHT][MAX_WIDTH];
   }
   
   public BarcodeImage (String[] str_data)
   {   
      this.image_data = new boolean[MAX_HEIGHT][MAX_WIDTH];
      
      int barStopRow = 0, barStopCol = 0, barStartRow = 0, barStartCol = 0;
      boolean breakflag = false;
      
      if(checkSize(str_data))
      {
         //Find str_data barcode endpoint
         for(int i = str_data.length -1; i >= 0; i--)
         {
            for (int j = str_data[0].length() - 1; j >=0; j--)
            
               if(str_data[i].charAt(j) == '*')
               {
                  barStopRow = i;
                  barStopCol = j;
                  breakflag = true;
                  break;
               }
            if(breakflag == true)
            {
               break;
            }
         }
      
         breakflag = false;
         //find str_data barcode start point
         for(int i = 0 ; i < str_data.length; i++)
         {
            for (int j = 0; j < str_data[0].length() ; j++)
            
               if(str_data[i].charAt(j) == '*')
               {
                  barStartRow = i;
                  barStartCol = j;
                  breakflag = true;
                  break;
               }
            if(breakflag == true)
            {
               break;
            }
         }

		 //copy string array and places valid data in bottom left of image_data 2D array
         int colIndex;
         for(int m = barStartRow; m <= barStopRow; m++)
         {
            colIndex = 0;
         
            for(int n = barStartCol; n <= barStopCol; n++)
            {
               if (str_data[m].charAt(n) == '*')
               {
                  this.setPixel(MAX_HEIGHT -(barStopRow - m) - 1, colIndex++, true);
               }
               else if (str_data[m].charAt(n) != '*')
               {
                  this.setPixel(MAX_HEIGHT -(barStopRow - m) - 1, colIndex++, false);
               }
            }
         }
      }
   }
   
   public Object clone()
   {
      try 
      {
         BarcodeImage copy = (BarcodeImage)super.clone();
         
         //clone performs a shallow copy on the array and requires looping through outer array and cloning inner contents
         copy.image_data = this.image_data.clone();
         for(int i = 0; i < this.image_data.length; i++)
         {
            copy.image_data[i] = this.image_data[i].clone();
         }
            return copy;
        } 
      catch (CloneNotSupportedException e) 
      {
           e.printStackTrace();
           throw new RuntimeException();
       }
   }
   
   //returns specified pixel
   public boolean getPixel(int row, int col)
   {
      if (row >= 0 && row < MAX_HEIGHT && col >= 0 && row < MAX_WIDTH )
      {
         return this.image_data[row][col];
      }
      else
      {
         return false;
      }
   }
   
   //sets specified pixel
   public boolean setPixel(int row, int col, boolean value)
   {
      if (row >= 0 && row < MAX_HEIGHT && col >= 0 && row < MAX_WIDTH )
      {
         this.image_data[row][col] = value;
         return true;
      }
      else
      {
         return false;
      }
   }
   
   //verfies the size of the data does not exceed max
   boolean checkSize(String[] data)
   {
      if (data == null)
      {
         return false;
      }
      else if (data.length > MAX_HEIGHT || data[0].length() > MAX_WIDTH)
      {
         return false;
      }
      else
      {
         return true;
      }
   }
   
   //displays image_data
   void dispalyToConsole()
   {
      for(int i = 0; i < MAX_HEIGHT; i++)
      {
         for (int j = 0; j < MAX_WIDTH; j++)
         {
            if (this.image_data[i][j])
            {
               System.out.print("[1]");
            }
            else
            {
               System.out.print("[0]");
            }
         }
         System.out.println();
      }
   }
   
   public static void main(String[] args) 
   {   
      String[] sImageIn =
      {
               "                                               ",
               "                                               ",
               "                                               ",
               "     * * * * * * * * * * * * * * * * * * * * * ",
               "     *                                       * ",
               "     ****** **** ****** ******* ** *** *****   ",
               "     *     *    ****************************** ",
               "     * **    * *        **  *    * * *   *     ",
               "     *   *    *  *****    *   * *   *  **  *** ",
               "     *  **     * *** **   **  *    **  ***  *  ",
               "     ***  * **   **  *   ****    *  *  ** * ** ",
               "     *****  ***  *  * *   ** ** **  *   * *    ",
               "     ***************************************** ",  
               "                                               ",
               "                                               ",
               "                                               "

            };      
                  
               
            
            String[] sImageIn_2 =
            {
                  "                                          ",
                  "                                          ",
                  "* * * * * * * * * * * * * * * * * * *     ",
                  "*                                    *    ",
                  "**** *** **   ***** ****   *********      ",
                  "* ************ ************ **********    ",
                  "** *      *    *  * * *         * *       ",
                  "***   *  *           * **    *      **    ",
                  "* ** * *  *   * * * **  *   ***   ***     ",
                  "* *           **    *****  *   **   **    ",
                  "****  *  * *  * **  ** *   ** *  * *      ",
                  "**************************************    ",
                  "                                          ",
                  "                                          ",
                  "                                          ",
                  "                                          "

            };
            
            BarcodeImage myCode = new BarcodeImage(sImageIn_2);
            myCode.dispalyToConsole();
            
            BarcodeImage myCode2 = (BarcodeImage) myCode.clone();
            
            myCode2.setPixel(0, 0, true);
            myCode.setPixel(0, 0, false);

            System.out.println(myCode2.getPixel(0, 0));
            System.out.println(myCode.getPixel(0, 0));
   }
}
