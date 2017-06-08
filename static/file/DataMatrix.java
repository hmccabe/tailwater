
public class DataMatrix implements BarcodeIO
{
   public static final char BLACK_CHAR = '*';
   public static final char WHITE_CHAR = ' ';
   private BarcodeImage image;
   private String text;
   private int actualWidth, actualHeight;
   
   //DefaultConstrucor - constructs an empty, but non-null, image and text value
   public DataMatrix()
   {
      this.text = "";
      this.image = new BarcodeImage();
      this.actualHeight = 0;
      this.actualWidth = 0;
   }
   
   //sets the image but leaves the text at its default value.
   public DataMatrix(BarcodeImage image)
   {
      scan(image);
   }
   
   //sets the text but leaves the image at its default value
   public DataMatrix(String text)
   {
      this.readText(text);
   }
   
   //Takes in a string variable and sets the data member "text"
   public boolean readText(String text)
   {
      this.text = text;
      return true;
   }
   
   //Sets image and calls helper methods to determine data members actualWidth and actualHeight
   public boolean scan(BarcodeImage image)
   {
      this.image = (BarcodeImage)image.clone();
      this.cleanImage();
      this.actualWidth = this.computeSignalWidth();
      this.actualHeight = this.computeSignalHeight();
      return true;
   }
   
   //returns actualWidth
   public int getActualWidth()
   {
      return this.actualWidth;
   }
   
   //returns actualHeight
   public int getActualHeight()
   {
      return this.actualHeight;
   }
   
   //returns width of image assuming it is in lower left corner
   private int computeSignalWidth()
   {
      return 1;
   }
   
   //returns height of image assuming it is in lower left corner
   private int computeSignalHeight()
   {
      return 1;
   }
   
   //moves the signal to the lower-left of the larger 2D array by calling
   //moveImage to LowerLeft
   private void cleanImage()
   {
      
   }
   
   //moves image to the lower left of the 2 -array by calling
   //shiftImageDown and shiftImageLeft
    private void moveImageToLowerLeft()
    {
       
    }
   
    //shifts image down by a specified offset
    private void shiftImageDown(int offset)
    {
       
    }
    
    //shift image to the left by a specified offset
    private void shiftImageLeft(int offset)
    {
       
    }
    
    //displays a cropped version of the original image leaving out whitespace
    public void displayImageToConsole()
    {
       
    }
    
    public void displayTextToConsole()
    {
       
    }
    
    public boolean generateImageFromText()
    {
       return true;
    }
    
    public boolean translateImageToText()
    {
       return true;
    }

}
