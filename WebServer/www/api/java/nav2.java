public class nav2{
    public static void main(String[] args){
        Robot r = new Robot();
	if(args.length < 1){
	    System.out.println("Usage java nav2.javac <landmark>");
	    return;
	}
	try{
	    r.navigateToLocation(args[0]);
	}catch(MapException e){
	    System.out.println("That is not a valid landmark");
	}
    }
}
