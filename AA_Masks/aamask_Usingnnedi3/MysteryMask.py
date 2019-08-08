from vapoursynth import core
import vapoursynth as vs

# made by some alchohol and barbecue
def Myst_aamask(clip,ts=1.5,ds_rate=1):
	lut_aamask = []
	for i in range(65536):
		if i*3>=65536:
			lut_aamask.append(65535)
		else:
			lut_aamask.append(3*i)
	clip = clip.std.ShufflePlanes( [0], colorfamily=vs.GRAY)
	cliptr = clip.std.Transpose()
	nn1 = clip.znedi3.nnedi3( field=0,dh=False,nsize=4,show_mask = True)
	nn2 = clip.znedi3.nnedi3( field=1,dh=False,nsize=4,show_mask = True)
	nnh = mvf.Max(nn1,nn2)
	nn1 = cliptr.znedi3.nnedi3( field=0,dh=False,nsize=4,show_mask = True)
	nn2 = cliptr.znedi3.nnedi3( field=1,dh=False,nsize=4,show_mask = True)
	nnw = mvf.Max(nn1,nn2).std.Transpose()
	nnmask = mvf.Max(nnw,nnh).std.Expr(['x 65535 = 65535 0 ?']).std.Convolution( matrix=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]).std.Expr(['x 20970 < 0 65535 ?']).resize.Bilinear(int(clip.width*ds_rate),int(clip.height*ds_rate))#
	nnmask = nnmask.sangnom.SangNom( order=1, aa=48, planes=[0]).rgvs.Repair(nnmask,1)
	nnmask_2 = nnmask.std.Convolution( matrix=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])#nnmask.rgvs.RemoveGrain(20)
	nnmask = core.std.Expr([nnmask_2,nnmask],['x 15730 < 0 y ?']).resize.Bilinear(clip.width,clip.height).std.Maximum().std.Minimum()#bicubic
	aamask = clip.tcanny.TCanny(ts, 20.0, 8.0, planes=[0]).rgvs.RemoveGrain(11).std.Lut([0], lut_aamask)
	black = core.std.BlankClip(width=clip.width, height=clip.height, format=vs.GRAY16, length=clip.num_frames, color=0).std.AssumeFPS(clip)
	ret = core.std.MaskedMerge(black, aamask, nnmask)
	#ret = mvf.ToYUV(ret,css='420',full=True,depth=16)	
	return ret